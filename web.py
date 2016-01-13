import cherrypy
import time

class OrbWeb(object):
    def __init__(self, queue, runner, cm):
        self.queue = queue
        self.runner = runner

        self.cm = cm

        self.show_library = show_library = {}

        for name in runner.shows:
            show_library[name] = s = {
                'type': "master"
            }
            if name in runner.random_eligible_shows:
                s['random'] = True

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
            'message': self.cm.message,
            'max_time': int(self.runner.max_show_time * 1000),
        }

        return out

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def server_reset(self):
        data = cherrypy.request.json

        if not data.get("please"):
            return {"ok": False, "msg": "You didn't say please"}

        return {"ok": True}

