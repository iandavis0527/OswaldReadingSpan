import cherrypy

from cherrypy_utils import domain
from cherrypy_utils import templating


# noinspection PyPep8Naming, PyMethodMayBeStatic
@cherrypy.expose
class RSPANView:
    def GET(self, subjectId="missing-subject-id", qualtrics=False):
        cherrypy.log("Inside RSPAN view")
        return templating.env.get_template("rspan.html.j2").render(
            subjectId=subjectId,
            qualtrics=str(qualtrics).lower(),
            domain=domain.get_domain_for_template(),
        )
