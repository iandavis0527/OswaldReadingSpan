import argparse
import os
import pathlib

from cherrypy_utils import docker_utils


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Utility script to build the digital deception docker container")
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Enable the debug build meant to be run from local host",
    )
    args = parser.parse_args()

    mount_source = "/home/mraUser/online_experiments_data"

    if args.debug:
        if not os.path.exists("./oswald_reading_data"):
            os.makedirs("./oswald_reading_data")

        mount_source = pathlib.Path(".").absolute().resolve()

    docker_utils.build_docker_container(
        "oswald_reading_span",
        version_number=docker_utils.get_version_number().replace("-", "."),
        mount=True,
        mount_source=mount_source,
        mount_folder="oswald_reading_data",
        mount_destination="/oswald_reading_data",
        restart_policy="unless-stopped",
        port_mappings={"5002": "5002"},
    )
