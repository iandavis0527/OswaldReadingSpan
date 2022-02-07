from oswald_reading_span.backend.configuration import base_config


def get_config():
    base = base_config.get_config()
    base["global"]["environment"] = "production"
    return base
