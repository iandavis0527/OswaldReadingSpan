import csv
import datetime
import io
import zipfile
import cherrypy

from cherrypy_utils import url_utils

from oswald_reading_span.backend.configuration import application_data
from oswald_reading_span.backend.export.collect_results import (
    collect_long_results,
    collect_results_summary,
    long_header,
    summary_header,
)


@cherrypy.expose
class ExperimentExportApi:
    def GET(self, subject_ids=None, mouse_events="False"):
        if not subject_ids:
            raise cherrypy.HTTPError(status=400, message="No subject id(s) provided!")

        app = application_data.get_app()

        if not app.user_is_authenticated():
            app.set_login_redirect(
                "api",
                "export?subject_ids={0}&mouse_events={1}".format(
                    ",".join(subject_ids),
                    mouse_events,
                ),
            )
            raise cherrypy.HTTPRedirect(url_utils.combine_url(app.subdomain, "login"))

        include_mouse_events = mouse_events.lower() == "true"

        subject_ids = subject_ids.replace(" ", "").split(",")

        output = io.StringIO()
        export_session_csv(
            output,
            cherrypy.request.databases["digital_deception"],
            subject_ids,
        )

        summary_output = io.StringIO()
        export_session_summary(
            summary_output,
            cherrypy.request.databases["digital_deception"],
            subject_ids,
        )

        cherrypy.response.status = "200 OK"

        archive_io = io.BytesIO()

        with zipfile.ZipFile(archive_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(self.get_main_filename(subject_ids), output.getvalue())
            zip_file.writestr(self.get_summary_filename(subject_ids), summary_output.getvalue())

        return self.serve_static(self.get_archive_filename(subject_ids), archive_io)

    def get_main_filename(self, subject_ids):
        return "rspan_export_{0}_{1}.csv".format("-".join(subject_ids), datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"))

    def get_summary_filename(self, subject_ids):
        return "rspan_summary_{0}_{1}.csv".format(
            "-".join(subject_ids), datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        )

    def get_archive_filename(self, subject_ids):
        return "rspan_export_{0}_{1}.zip".format(
            "-".join(subject_ids[:4]),
            datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"),
        )


def export_session_csv(output, session, subject_ids):
    results = collect_long_results(session, subject_ids)

    with csv.writer(output) as writer:
        writer.writerow(long_header())

        for record in results.all():
            writer.writerow(record)


def export_session_summary(output, session, subject_ids):
    results = collect_results_summary(session, subject_ids)

    with csv.writer(output) as writer:
        writer.writerow(summary_header())

        for record in results.all():
            writer.writerow(record)
