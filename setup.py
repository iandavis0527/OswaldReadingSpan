import subprocess
import pathlib

from setuptools import find_packages, setup


def install_and_build(path):
    subprocess.run(["npm", "install"], cwd=path)
    subprocess.run(["npm", "run-script", "build"], cwd=path)


print("Building ReactJS Frontend")
install_and_build(pathlib.Path("oswald_reading_span", "frontend"))

setup(
    name="oswald_reading_span",
    packages=find_packages(),
    version="1.0.0",
    description="Cherrypy web server plugin for the oswald shortened reading span task",
    author="Me",
    license="MIT",
    include_package_data=True,
    install_requires=[
        "cherrypy",
        "cherrypy_utils @ git+https://git.mindmodeling.org/ian.davis/CherrypyUtils.git",
        "python-ldap",
        "sqlalchemy",
        "jinja2",
    ],
)
