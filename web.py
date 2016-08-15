import cherrypy
import time

class OrbWeb(object):
    def __init__(self, queue, runner, cm, wc):
        self.queue = queue
        self.runner = runner

        self.cm = cm
        self.wc = wc

        self.show_library = show_library = {}

        for name in runner.shows:
            show_library[name] = s = {
                'type': "master",
            }
            if hasattr(runner.shows[name],'controls'):
                show_library[name]['controls'] = runner.shows[name].controls
            if name in runner.random_eligible_shows:
                s['random'] = True

        for name in runner.overlay_shows:
            show_library[name] = s = {
                'type': "overlay",
            }


    @cherrypy.expose
    def clear_show(self):
        self.queue.put("clear")
        return "<a href='.'/>Back</a>"

    @cherrypy.expose
    def change_run_time(self, run_time=None):
        try:
            print "RUNTIME XXXXX:::: %s" % run_time
            run_time = int(run_time)
            self.queue.put("inc runtime:%s"%run_time)
        except Exception as e:
            print "\n\nCRASH\n\n", e
            #probably a string... do nothing!
            pass
        return "<a href='.'/>Back</a>"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def run_overlay(self):
        data = cherrypy.request.json
        name = data.get("name")
        if name:
            self.queue.put("run_overlay:"+name)
            print "Setting overlay to:", name
        else:
            print "Didn't get a overlay name"

        return {'ok': True}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stop_overlay(self):

        self.queue.put("stop_overlay")
        print "Stopping all overlays"

        return {'ok': True}


    @cherrypy.expose
    def run_show(self, show_name=None):
        if show_name:
            self.queue.put("run_show:"+show_name)
            print "Setting show to:", show_name
        else:
            print "Didn't get a show name"

        # XXX otherwise the runner.status() method
        # hasn't had time to update
        time.sleep(0.2)
        raise cherrypy.HTTPRedirect("/")


    @cherrypy.expose
    def admin(self):
        raise cherrypy.HTTPRedirect("/static/admin.html")

    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def shows(self):
        return self.show_library

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start_show(self):
        data = cherrypy.request.json
        name = data.get("name")
        print "Start show name='%s'" % name

        self.runner.next_show(name=name)

        return {'ok': True}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status(self):

        out = {
            'show': {
                'name': self.runner.show.name,
                'run_time': int(self.runner.show_runtime * 1000)
            },
            'max_time': int(self.runner.max_show_time * 1000),
            'speed': self.cm.speed_multi,
            'brightness': self.cm.brightness
        }

        return out

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def shutdown(self):
        try:
            data = cherrypy.request.json
        except:
            return {"ok": False, "msg": "You didn't say please"}

        if not data.get("please"):
            return {"ok": False, "msg": "You didn't say please"}

        import os
        os.system("shutdown -h now")
        print "SHUTDOWN"

        return {"ok": True}


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def server_reset(self):
        try:
            data = cherrypy.request.json
        except:
            return {"ok": False, "msg": "You didn't say please"}

        if not data.get("please"):
            return {"ok": False, "msg": "You didn't say please"}

        return {"ok": True}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def config(self):
        """ test with:

       curl -X POST    -H "Content-Type: application/json" -d '{"command": "set_color", "ix": 0, "color": "red"}' http://192.168.30.162:1072/config

        """

        try:
            data = cherrypy.request.json
        except:
            return {"ok": False, "msg": "No data provided"}

        if not data.get("command"):
            return {"ok": False, "msg": "Tell me what to do!"}

        command = data.get("command")
        if command == "set_color":
            ix = data.get("ix",0)
            color = data.get("color", "5050ff")
            self.wc.set_color(ix, color)

            return {"ok": True, "done": "set color %s to %s" % (ix, color)}
           
        elif command == "set_speed":
            speed = data.get("speed",0)
            self.wc.set_speed(speed)
            return {"ok": True, "done": "change speed to %s" % (self.cm.speed_multi), 'speed': self.cm.speed_multi}

        elif command == "set_brightness":
            brightness = data.get("brightness",0)
            self.wc.set_brightness(brightness)
            return {"ok": True, "done": "change brightness to %s" % (self.cm.brightness), 'brightness': self.cm.brightness}

        elif command == "set_max_runtime":
            max_time = data.get("runtime",0)
            self.wc.set_max_runtime(max_time)
            return {"ok": True, "done": "change max runtime to %s" % (self.cm.max_time), 'max_runtime': self.cm.max_time}

        elif command == "set_range":
            value = data.get("value",0)
            range = data.get("range",0)
            self.wc.set_custom_range_value(range, value)
            return {"ok": True, "done": "change range %s value to %s" % (range, value)}

        elif command == "set_checkbox":
            value = data.get("value",0)
            checkbox = data.get("checkbox",0)
            self.wc.set_custom_checkbox_value(checkbox, value)
            return {"ok": True, "done": "change checkbox %s value to %s" % (checkbox, value)}

        elif command == "set_config":
            command = data.get("command",0)
            value = data.get("value",0)
            self.wc.set_config(command, value)
            return {"ok": True, "done": "change fc config %s to %s" % (command, value)}


        else:
            return {"ok": False, "msg": "Not a command I know"}





