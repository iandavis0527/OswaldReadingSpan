import cherrypy

from oswald_reading_span.backend.configuration import application_data


# noinspection PyPep8Naming, PyMethodMayBeStatic
class LoginView:
    @cherrypy.expose
    @cherrypy.tools.allow(methods=["POST"])
    def post(self, username=None, password=None):
        app = application_data.get_app()

        status = app.authenticate_user(username, password)

        if status:
            cherrypy.response.status = "200 Ok"
            return "true"
        else:
            cherrypy.response.status = "403 Forbidden"
            return "false"

    @cherrypy.expose
    def status(self):
        app = application_data.get_app()

        if app.user_is_authenticated():
            cherrypy.response.status = "200 Ok"
            return "true"
        else:
            cherrypy.response.status = "200 Ok"
            return "false"
