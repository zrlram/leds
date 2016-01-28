#!/usr/bin/python

import threading
import sys
import Queue
import traceback
import time
import signal

import cProfile

import shows
from model import Model
from web_controller import WebController
import controls_model

# Ideas and a bunch of code borrowed from https://github.com/baaahs/lights


def _stacktraces(signum, frame):
    txt = []
    for threadId, stack in sys._current_frames().items():
        txt.append("\n# ThreadID: %s" % threadId)
        for filename, lineno, name, line in traceback.extract_stack(stack):
            txt.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                txt.append("  %s" % (line.strip()))

    print "\n".join(txt)

signal.signal(signal.SIGQUIT, _stacktraces)


class ShowRunner(threading.Thread):

    def __init__(self, geometry, queue, cm, wc, max_showtime=240):
        super(ShowRunner, self).__init__(name="ShowRunner")

        self.profile = None
        self.do_profiling = True

        self.geometry = geometry
        self.queue = queue
        self.cm = cm
        self.wc = wc

        self.cm.add_listener(self)
        self.cm.show_runner = self 

        self.running = True
        self.max_show_time = max_showtime

        self.shows = dict(shows.load_shows())
        self.random_eligible_shows = []

        for name in self.shows:
            _class = self.shows[name]

            ok_for_random = True
            if hasattr(_class, "ok_for_random"):
                ok_for_random = _class.ok_for_random

            if ok_for_random:
                self.random_eligible_shows.append(name)

        print "Shows: %s" % ', '.join([s for s in self.shows])
        print "Random eligible shows: %s" % str(self.random_eligible_shows)

        self.randseq = self.random_show_name()
        
        self.show = None                        # current show object 
        self.framegen = None                    # next frame... (next_frame)

        # show speed multiplier - ranges from 0.5 to 2.0
        # 1.0 is normal speed
        # lower numbers mean faster speeds, higher is slower
        self.speed_x = 1.0

        self.cm.set_max_time(self.max_show_time)

    def next_show(self, name=None):

        if self.profile:
            # Stop it
            print "****** Stopping profiling"
            self.profile.disable()
            self.profile.dump_stats("Stats")
        elif self.do_profiling:
            # Start a profiler
            self.do_profiling = False
            self.profile = cProfile.Profile()
            print "****** Starting profiling"
            self.profile.enable()

        show = None
        if name:
            if name in self.shows:
                show = self.shows[name]

            else:
                print "Unknown show:", name

        if not show:
            print "Choosing random show"
            name = self.randseq.next()
            show = self.shows[name]

        self.clear()
        self.prev_show = self.show

        # unregister shaders
        self.geometry.reset_shaders()

        self.show = show(self.geometry)
        print "Next show:" + self.show.name
        self.framegen = self.show.next_frame()
        try:
            self.show.start()    # if show has a start() call it. Registers shaders, etc.
        except:
            pass

        self.show_runtime = 0

        # deal with controls
        self.cm.del_listener(self.prev_show)
        self.cm.add_listener(self.show)
        try:
            self.show.set_controls_model(self.cm)
        except AttributeError:
            pass

        try:
            self.show.control_refreshAll()
        except AttributeError:
            pass

        self.cm.set_show_name(name)


    def get_next_frame(self):
        ''' returns a delay or None '''
        try:
            return self.framegen.next()
        except StopIteration:
            return None
   
    def random_show_name(self):
        """
        Return an infinite sequence of randomized show names
        Remembers the last 'norepeat' items to avoid replaying shows too soon
        Norepeat defaults to 1/3 the size of the sequence
        """
        seq = self.random_eligible_shows

        norepeat=int(len(seq)/3)
        if norepeat < 1:
            norepeat = 1

        import random
        seen = []
        while True:
            n = random.choice(seq)
            while n in seen:
                n = random.choice(seq)
            seen.append(n)
            while len(seen) >= norepeat:
                seen.pop(0)
            yield n

    def run(self):

        if not (self.show and self.framegen):
            self.next_show()

        next_frame_at = 0.0                           
        show_started_at = time.time()

        while self.running:
            try:

                self.check_queue()

                start = time.time()
                self.show_runtime = start - show_started_at

                if start >= next_frame_at:
                    # print "%f next frame" % start
                    delta = self.get_next_frame()

                    # If they give us an advisory time, we will record it, otherwise
                    # we will keep asking for frames as quickly as we can
                    if delta:
                        next_frame_at = time.time() + (delta * self.speed_x)

                else:
                    # print "%f not yet" % start
                    pass

                # Maybe this show is done?
                if self.show_runtime > self.max_show_time:
                    print "Max show time elapsed, changing shows"
                    self.next_show()
                    next_frame_at = show_started_at = time.time()
                else:
                    # Not a new show yet, so we are going to pause, but never
                    # more that .023s which yields roughly the max DMX framerate
                    # of 44hz

                    # TBD -- need to do some profiling here. Do we really have the luxury of sleepign ???
                    to_sleep = 0.023 
                    until_next = next_frame_at - time.time()

                    if until_next < to_sleep and until_next > 0.001:
                        to_sleep = until_next

                    # print "toSleep = %s" % str(to_sleep)
                    time.sleep(to_sleep)

            except Exception:
                print "Unexpected exception in show loop!"
                traceback.print_exc()
                self.next_show()

    def control_speed_changed(self):
        print "Setting default show speed to %f" % self.cm.speed_multi

        # speed_x is opposite of speedMulti, so we have to invert speedMulti
        self.speed_x = 1.0 / self.cm.speed_multi

    def control_max_time_changed(self):
        self.max_show_time = int(self.cm.max_time)

    def control_brightness_changed(self, val):
        self.geometry.set_brightness(val)

    def status(self):

        if self.running:
            return "Running: %s (%d seconds left)" % (self.show.name, self.max_show_time - self.show_runtime)
        else:
            return "Stopped"

    # because we have threading give commands a chance to be worked on. 
    def check_queue(self):
        msgs = []
        try:
            while True:
                m = self.queue.get_nowait()
                if m:
                    msgs.append(m)

        except Queue.Empty:
            pass

        if msgs:
            for m in msgs:
                self.process_command(m)

    def process_command(self, msg):

        if isinstance(msg, basestring):
            if msg == "shutdown":
                self.running = False
                print "ShowRunner shutting down"
            elif msg == "clear":
                self.clear()
                time.sleep(2)
            elif msg.startswith("run_show:"):
                self.running = True
                show_name = msg[9:]
                self.next_show(show_name)
            elif msg.startswith("inc runtime"):
                self.max_show_time = int(msg.split(':')[1])

        else:
            print "ignoring unknown msg:", str(msg)

    def clear(self):
        self.geometry.clear()

class Server(threading.Thread):
    def __init__(self, geometry, args):
        self.args = args
        self.geometry = geometry 

        # this is going to be the ShowRunner 
        self.runner = None
        self.queue = Queue.LifoQueue()
        self.controls_model = controls_model.ControlsModel()
        self.wc = WebController(self.controls_model)
 
        self.running = False
        self._create_services()


    def _create_services(self):

        self.runner = ShowRunner(self.geometry, self.queue, self.controls_model, self.wc)

        # invoking specific shows from command line
        if args.shows:
            print "Setting show:", args.shows[0]
            self.runner.next_show(args.shows[0]) 

    def start(self):

        if self.running:
            print "start() called, but orb is already running!"
            return

        try:
            self.runner.start()
            self.running = True

        except Exception, e:
            print "Exception starting orb!"
            traceback.print_exc()

    def stop(self):

        if self.running: # should be safe to call multiple times
            try:
                self.queue.put("shutdown")
                self.running = False

            except Exception, e:
                print "Exception stopping orb!"
                traceback.print_exc()

    def start_headless(self):

        "Run without the web interface"
        print "Running without web interface"
        try:
            while True:
                time.sleep(999) # control-c breaks out of time.sleep
        except KeyboardInterrupt:
            print "Exiting on keyboard interrupt"

        self.stop()

    def start_web(self):
        "Starting Web interface"
        import cherrypy
        import os
        from web import OrbWeb

        cherrypy.engine.subscribe('stop', self.stop)

        port = 1072
        _dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "web", "static"))
        print _dir

        config = {
            'global': {
                'server.socket_host' : '0.0.0.0',
                'server.socket_port' : port,
                # 'engine.timeout_monitor.on' : True,
                # 'engine.timeout_monitor.frequency' : 240,
                # 'response.timeout' : 60*15
            },

            '/index': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': os.path.join(_dir, "index.html")
            },

            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': _dir
            }
        }

        # this method blocks until KeyboardInterrupt
        cherrypy.quickstart(OrbWeb(self.queue, self.runner, self.controls_model, self.wc),
                            '/',
                            config=config)

        # turn off logging (speed up?)
        cherrypy.config.update({ "environment": "embedded" })

if __name__=='__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Orb Control Center')

    parser.add_argument('--list', action='store_true', help='List available shows')
    parser.add_argument('shows', metavar='show_name', type=str, nargs='*',
                        help='name of show (or shows) to run')
    parser.add_argument('--headless', action='store_true', default=False,
                        help='run headless or with web')
    
    args = parser.parse_args()

    if args.list:
        print "Available shows:"
        print ', '.join([s[0] for s in shows.load_shows()])
        sys.exit(0)

    geometry = Model('sphere_10.json')
    app = Server(geometry, args)

    try:
        app.start()     # start related service threads
        if args.headless:
            app.start_headless()
        else:
            app.start_web()

    except Exception, e:
        print "Unhandled exception running orb!"
        traceback.print_exc()

    finally:
        app.stop()
