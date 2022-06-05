import argparse
import json
import pathlib
import cherrypy

from cherrypy_utils import url_utils
from cherrypy_utils.cherrypy_sqlalchemy_utils import SQLAlchemyTool, SQLAlchemyPlugin
from cherrypy_utils.database import Base

from oswald_reading_span.backend.api import RSPANTestApi
from oswald_reading_span.backend.export.api import RSPANExportDownload
from oswald_reading_span.backend.export.views import RSPANExportView
from oswald_reading_span.backend.login.views import LoginView
from oswald_reading_span.backend.models.sentences import ReadingSpanSentence
from oswald_reading_span.backend.views import RSPANView
from oswald_reading_span.backend.configuration import application_data, production_config, development_config


def initialize_db(session):
    ReadingSpanSentence.initialize_sentences(session)


def setup_server(subdomain="", shared_data_location=None, production=False):
    server_directory = pathlib.Path(__file__).parent.absolute()
    template_location = server_directory.joinpath("frontend", "main", "templates")
    api_key_filepath = server_directory.joinpath("backend", "configuration", "api.key")

    if not shared_data_location:
        shared_data_location = server_directory

    cherrypy.log("=" * 100)
    cherrypy.log("OSWALD READING SPAN INIT SECTION")
    cherrypy.log("-" * 100)
    cherrypy.log("server_root found at {0}".format(server_directory))
    cherrypy.log("shared data root at {0}".format(shared_data_location))

    application_data.initialize(
        subdomain=subdomain,
        application_location=server_directory,
        shared_data_location=server_directory,
        template_location=template_location,
        api_key_filepath=api_key_filepath,
        production=production,
    )

    cherrypy._cpconfig.environments["production"]["log.screen"] = True

    if production:
        cherrypy.log("Using production configuration")
        active_file = production_config.get_config()
    elif not production:
        cherrypy.log("Using development configuration")
        active_file = development_config.get_config()

    cherrypy._cperror._HTTPErrorTemplate = cherrypy._cperror._HTTPErrorTemplate.replace(
        'Powered by <a href="http://www.cherrypy.org">CherryPy %(version)s</a>\n', ""
    )
    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.tools.oswald_reading_database = SQLAlchemyTool("oswald_reading")

    cherrypy.tree.mount(
        LoginView(),
        url_utils.combine_url(subdomain, "export", "login"),
        {
            "/": {"tools.sessions.on": True},
        },
    )
    cherrypy.tree.mount(
        RSPANExportDownload(),
        url_utils.combine_url(subdomain, "export", "download"),
        {
            "/": {
                "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
                "tools.sessions.on": True,
                "tools.oswald_reading_database.on": True,
            },
        },
    )
    cherrypy.tree.mount(RSPANView(), subdomain, active_file)
    cherrypy.tree.mount(
        RSPANTestApi(),
        url_utils.combine_url(subdomain, "api", "result"),
        {
            "/": {
                "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
                "tools.require_api_key.on": True,
                "tools.response_headers.on": True,
                "tools.response_headers.headers": [("Content-Type", "application/json")],
                "tools.json_in.on": True,
                "tools.json_out.on": True,
                "tools.oswald_reading_database.on": True,
            }
        },
    )

    mysql_filepath = server_directory.joinpath("backend", "configuration", "mysql.credentials").resolve()

    # mysql connection:
    # mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
    if production and mysql_filepath.exists():
        with open(mysql_filepath, "r") as mysql_credentials_file:
            credentials = json.load(mysql_credentials_file)
            connection_string = str("mysql+pymysql://{username}:{password}@{host}/{db_name}").format_map(credentials)
    else:
        cherrypy.log("Using sqlite database file in lieu of mysql credentials!")
        database_filepath = str(pathlib.Path(shared_data_location, "digital_deception.db").resolve())
        connection_string = "sqlite:///" + database_filepath

    SQLAlchemyPlugin(
        "oswald_reading",
        cherrypy.engine,
        Base,
        connection_string,
        echo=True,
        pool_recycle=20000,
        after_engine_setup=initialize_db,
    )

    cherrypy.log("Publishing db create for oswald_reading")
    cherrypy.engine.publish("oswald_reading.db.create")

    cherrypy.log("END OSWALD READING SPAN INIT")
    cherrypy.log("=" * 100)


def run(subdomain="/digital-deception/rspan", production=False, shared_data_location=None, port=8080):
    old_mount_function = cherrypy.tree.mount

    def _monkey_mount(handler, url, config_file):
        cherrypy.log("Mounting URL {0}".format(url))
        old_mount_function(handler, url, config_file)

    cherrypy.tree.mount = _monkey_mount

    setup_server(subdomain=subdomain, production=production, shared_data_location=shared_data_location)

    cherrypy.log("setting server port to:" + str(port))
    cherrypy.config.update({"server.socket_port": port})

    cherrypy.engine.signals.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Run the Reading Span web server")
    parser.add_argument("--subdomain", default="/digital-deception/rspan", help="The sub domain to mount the app at")
    parser.add_argument("--production", default=False, action="store_true", help="Enable production mode")
    parser.add_argument("--shared_data_location", help="The location of the root shared data folder")
    parser.add_argument("--port", type=int, help="The port to listen on", default=8080)
    args = parser.parse_args()
    run(
        subdomain=args.subdomain,
        production=args.production,
        shared_data_location=args.shared_data_location,
        port=args.port,
    )
