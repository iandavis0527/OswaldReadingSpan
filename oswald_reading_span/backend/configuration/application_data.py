from cherrypy_utils import application_data


APP_NAME = "oswald_reading_span"


def get_app():
    return application_data.get_app(APP_NAME)


def initialize(
    subdomain,
    application_location,
    shared_data_location,
    template_location,
    api_key_filepath,
    production=True,
):
    return application_data.initialize(
        application_name=APP_NAME,
        subdomain=subdomain,
        application_location=application_location,
        shared_data_location=shared_data_location,
        template_location=template_location,
        api_key_filepath=api_key_filepath,
        production=production,
    )
