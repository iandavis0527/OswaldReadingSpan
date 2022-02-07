import cherrypy

from oswald_reading_span.backend.configuration import application_data

# noinspection PyPep8Naming, PyMethodMayBeStatic
@cherrypy.expose
class RSPANView:
    def GET(self, subjectId="missing-subject-id", qualtrics=False):
        cherrypy.log("Inside RSPAN view")
        print(cherrypy.request.app.config)

        return (
            application_data.get_app()
            .template_engine.get_template("rspan.html.j2")
            .render(
                subjectId=subjectId,
                qualtrics=str(qualtrics).lower(),
                domain=application_data.get_app().template_domain(),
            )
        )
