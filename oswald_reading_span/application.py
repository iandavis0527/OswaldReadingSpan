import argparse
import json
import os
import pathlib
import cherrypy

from cherrypy_utils import url_utils
from cherrypy_utils.cherrypy_sqlalchemy_utils import SQLAlchemyTool, SQLAlchemyPlugin
from cherrypy_utils.database import Base

from oswald_reading_span.backend.api import RSPANTestApi
from oswald_reading_span.backend.models.sentences import ReadingSpanSentence
from oswald_reading_span.backend.views import RSPANView
from oswald_reading_span.backend.configuration import application_data, production_config, development_config


def initialize_db(session):
    ReadingSpanSentence.initialize_sentences(session)


def setup_server(subdomain="", shared_data_location=None, production=False):
    server_directory = pathlib.Path(__file__).parent.absolute()
    template_location = server_directory.joinpath("frontend", "templates")
    api_key_filepath = server_directory.joinpath("backend", "configuration", "api.key")

    if not shared_data_location:
        shared_data_location = server_directory

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

    cherrypy.tree.mount(RSPANView(), subdomain, active_file)
    cherrypy.tree.mount(RSPANTestApi(), url_utils.combine_url(subdomain, "api", "result"), active_file)

    mysql_filepath = str(server_directory.joinpath("backend", "configuration", "mysql.credentials").resolve())

    # mysql connection:
    # mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
    if os.path.exists(mysql_filepath):
        with open(mysql_filepath, "r") as mysql_credentials_file:
            credentials = json.load(mysql_credentials_file)
            connection_string = str("mysql+pymysql://{username}:{password}@{host}/{db_name}").format_map(credentials)
    else:
        cherrypy.log("Using sqlite database file in lieu of mysql credentials!")
        database_filepath = str(shared_data_location.joinpath("digital_deception.db").resolve())
        connection_string = "sqlite:///" + database_filepath

    SQLAlchemyPlugin(
        "oswald_reading",
        cherrypy.engine,
        Base,
        connection_string,
        echo=False,
        pool_recycle=20000,
        after_engine_setup=initialize_db,
    )

    cherrypy.log("Publishing db create for digital_deception")
    cherrypy.engine.publish("digital_deception.db.create")


def run(production=False):
    setup_server(production=production)

    cherrypy.engine.signals.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Run the Reading Span web server")
    parser.add_argument("--production", action="store_true", help="Enable production mode")
    args = parser.parse_args()
    run(production=args.production)
