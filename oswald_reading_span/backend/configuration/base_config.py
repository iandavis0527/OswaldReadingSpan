import cherrypy
import pathlib


def get_config():
    return {
        "/": {
            "tools.encode.on": True,
            "tools.encode.encoding": "utf-8",
            "tools.oswald_reading_database.on": True,
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
            "request.show_tracebacks": True,
            "tools.staticdir.root": pathlib.Path(__file__).parent.parent.parent.joinpath("frontend", "main").resolve(),
        },
        "/export": {
            "tools.staticdir.root": pathlib.Path(__file__)
            .parent.parent.parent.joinpath("frontend", "export")
            .resolve(),
        },
        "/api": {
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "application/json")],
        },
        "global": {
            "engine.autoreload.on": False,
        },
        "/static": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": pathlib.Path("dist"),
        },
        "/api/result": {
            "tools.require_api_key.on": True,
            "tools.json_in.on": True,
            "tools.json_out.on": True,
        },
    }
