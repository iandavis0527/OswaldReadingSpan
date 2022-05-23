import csv
import datetime
import io
import zipfile
import cherrypy

from cherrypy.lib import static

from oswald_reading_span.backend.configuration import application_data
from oswald_reading_span.backend.export.collect_results import (
    collect_long_results,
    collect_results_summary,
    long_header,
    summary_header,
)


@cherrypy.expose
class RSPANExportDownload:
    def GET(self, subject_ids=None):
        app = application_data.get_app()

        if not app.user_is_authenticated():
            raise cherrypy.HTTPError(status=403, message="You must be signed in to export subject data")
        elif not subject_ids:
            raise cherrypy.HTTPError(status=400, message="No subject id(s) provided!")

        subject_ids = subject_ids.replace(" ", "").split(",")

        summary_output = io.StringIO()
        export_session_summary(
            summary_output,
            cherrypy.request.databases["oswald_reading"],
            subject_ids,
        )

        cherrypy.response.status = "200 OK"

        archive_io = io.BytesIO()

        with zipfile.ZipFile(archive_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for subject_id in subject_ids:
                output = io.StringIO()
                export_session_csv(
                    output,
                    cherrypy.request.databases["oswald_reading"],
                    (subject_id,),
                )

                zip_file.writestr(self.get_main_filename([subject_id]), output.getvalue())

            zip_file.writestr(self.get_summary_filename(subject_ids), summary_output.getvalue())

        return self.serve_static(self.get_archive_filename(subject_ids), archive_io)

    def serve_static(self, filename, data: io.BytesIO):
        cherrypy.log("Seeking stringio file-object back to beginning")
        data.seek(0)
        # encoded_output = io.BytesIO(data.read().encode("utf8"))
        # encoded_output.seek(0)
        return static.serve_fileobj(data, "application/x-download", "attachment", filename, debug=True)

    def get_main_filename(self, subject_ids):
        return "rspan_export_{0}_{1}.csv".format(
            "-".join(subject_ids), datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        )

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
    writer = csv.writer(output)
    writer.writerow(long_header())

    if not isinstance(results, list):
        results = results.all()

    for record in results:
        writer.writerow(record)


def export_session_summary(output, session, subject_ids):
    results = collect_results_summary(session, subject_ids)
    writer = csv.writer(output)
    writer.writerow(summary_header())

    for record in results.all():
        writer.writerow(record)
