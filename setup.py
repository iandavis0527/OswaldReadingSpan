import subprocess
import pathlib
import subprocess

from setuptools import find_packages, setup
from setuptools.command.install import install


frontend = pathlib.Path("oswald_reading_span", "frontend")


class NPMInstall(install):
    def run(self):
        subprocess.run(["npm", "install"], cwd=frontend.resolve(), capture_output=True)
        subprocess.run(["npm", "run-script", "build"], cwd=frontend.resolve(), capture_output=True)
        install.run(self)


class PostInstallCommand(install):
    def run(self):
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
    version="1.0.16",
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
