import cherrypy

from cherrypy_utils import domain

from oswald_reading_span.backend.configuration.base_config import get_template_environment

# noinspection PyPep8Naming, PyMethodMayBeStatic
@cherrypy.expose
class RSPANView:
    def GET(self, subjectId="missing-subject-id", qualtrics=False):
        cherrypy.log("Inside RSPAN view")
        return (
            get_template_environment()
            .get_template("rspan.html.j2")
            .render(
                subjectId=subjectId,
                qualtrics=str(qualtrics).lower(),
                domain=domain.get_domain_for_template(),
            )
        )
