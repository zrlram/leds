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
            print data
            ix = data.get("ix",0)
            color = data.get("color", "blue")
            self.wc.set_color(ix, color)

            return {"ok": True, "done": "set color %s to %s" % (ix, color)}

        else:
            return {"ok": False, "msg": "Not a command I know"}

        return {"ok": False}


