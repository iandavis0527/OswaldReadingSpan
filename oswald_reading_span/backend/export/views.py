import cherrypy


@cherrypy.expose
class RSPANExportView(object):
    def GET(self):
        pass


@cherrypy.expose
class RSPANLoginView(object):
    def POST(self, username, password):
        pass
