import pathlib
import json
import datetime
import subprocess

from setuptools import find_packages, setup
from setuptools.command.install import install

frontend = pathlib.Path("oswald_reading_span", "frontend")
main = pathlib.Path(frontend, "main")
export = pathlib.Path(frontend, "export")
common = pathlib.Path(frontend, "common")

package_data_filepath = pathlib.Path("package_data.json")
npm_package_filepaths = [
    pathlib.Path(frontend, "common", "package.json"),
    pathlib.Path(frontend, "export", "package.json"),
    pathlib.Path(frontend, "main", "package.json"),
]

version = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")


def npm_build(project_path):
    subprocess.run(
        ["npm", "install"],
        cwd=project_path.resolve(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    subprocess.run(
        ["npm", "run-script", "build"],
        cwd=project_path.resolve(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def update_version_numbers(version_number):
    global version
    version = version_number

    with open(package_data_filepath) as package_data_file:
        package_data = json.load(package_data_file)
        package_data["version"] = version_number.replace("-", ".")

    with open(package_data_filepath, "w") as package_data_file:
        json.dump(package_data, package_data_file, indent=4)

    for npm_package_filepath in npm_package_filepaths:
        with open(npm_package_filepath) as package_data_file:
            package_data = json.load(package_data_file)
            package_data["version"] = version_number.replace("-", ".")

        with open(npm_package_filepath, "w") as package_data_file:
            json.dump(package_data, package_data_file, indent=4)


class NPMInstall(install):
    def run(self):
        npm_build(common.resolve())
        npm_build(export.resolve())
        npm_build(main.resolve())
        install.run(self)


class PostInstallCommand(install):
    user_options = install.user_options + [
        ("version=", None, "The version number for this package"),
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.version = version

    def finalize_options(self):
        install.finalize_options(self)

    def run(self):
        if self.version:
            print("Updating package version numbers to {0} provided by pip install-option".format(self.version))
            update_version_numbers(self.version)

        print("Building ReactJS Frontend...")
        self.run_command("npm_install")
        install.run(self)


setup(
    cmdclass={
        "install": PostInstallCommand,
        "npm_install": NPMInstall,
    },
    name="oswald_reading_span",
    packages=find_packages(),
    version=version,
    description="Cherrypy web server plugin for the oswald shortened reading span task",
    author="Me",
    license="MIT",
    include_package_data=True,
    install_requires=[
        "cherrypy",
        "cherrypy_utils @ git+ssh://gitea@git.mindmodeling.org/ian.davis/CherrypyUtils.git",
        "python-ldap",
        "sqlalchemy",
        "jinja2",
        "pymysql",
    ],
)
