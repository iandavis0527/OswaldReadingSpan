# OswaldReadingSpan
A web-based implementation of the Oswald Reading Span task, derived from: https://englelab.gatech.edu/shortenedtasks.html

# Setup
## Required dependencies
The Oswald Reading Span task require the following high level dependencies:
* Python 3.6+: https://www.python.org/downloads/
* Cherrypy: https://docs.cherrypy.dev/en/latest/
* NodeJS (NPM) 16.15.1+: https://nodejs.org/en/download/

The backend requires several python package dependencies, which can be installed using pip and the requirements.txt file:
```
    pip install -r requirements.txt
```

The frontend requires several NPM package dependencies, which can be installed using npm and the package.json file located at `/oswald_reading_span/frontend/span task/`
```
    npm install
````

Once all dependencies are prepared, you can run the span task using `python -m oswald_reading_span.application`. You should see output similar to:
```
    [07/Jul/2022:11:16:17] ENGINE Bus STARTING
    [07/Jul/2022:11:16:17] ENGINE Serving on http://0.0.0.0:8080
    [07/Jul/2022:11:16:17] ENGINE Bus STARTED
```

You can then navigate your browser to http://localhost:8080/digital-deception/rspan?subjectId=test123

## Optional Dependencies
Support for Docker is available, and can be enabled by installing Docker: https://www.docker.com/. Once installed, point Docker to the Dockerfile at the root of the repository to build. Additionally, a python utility script [build_docker_container.py](https://github.com/iandavis0527/OswaldReadingSpan/blob/master/build_docker_container.py) encapsulates several commonly repeated commands and options.

# Backend
## Overview
The backend portion of the Oswald Span Tasks, located under `/oswald_reading_span/backend`, encapsulates the Cherrypy web server that hosts the span task code for the web. Backend responsibilities include:
* Serving HTTP Requests
* Querying a SQL Database using SQLAlchemy
* Rendering HTML templates using Jinja2
* Handling LDAP login authentication for data exports
* Serving file downloads for data exports
* Storing experiment results from the frontend in the database

## URLs
The cherrypy server consists of a collection of URLs, which can be referenced in entirety within /oswald_reading_span/application.py. A short list of the available urls (relative to the server root):
* `/digital-deception/rspan?test_id={testId}&debug={false}`: The main span task endpoint, with the test id parameter to separate the data for each concurrent run of the experiment. Normally, the span task expects to be embedded within a qualtrics survey and receive a randomized order for its feed from said survey. To disable this functionality, pass the debug parameter as true.
* `/digital-deception/practice?testId={testId}&debug={false}`: A special practice version of the span task useful for experiments. The parameters here are identical to the main endpoint above.
* `/digital-deception/rspan/export`: The experimenter dashboard. Current main function is to export available data from the task. Requires an LDAP login, or redirects to /digital-deception/rspan/login if not logged in. See `/oswald_reading_span/frontend/export` for the ReactJS project that creates the export dashboard.
* `/digital-deception/rspan/export/download?subjectIds={subjectIds}`: endpoint that exports subject data to CSV. Requires an LDAP login, and requires a comma separated list of subject ids as a url parameter.
* `/digital-deception/login`: Presents a login form and tries to login the user using LDAP.
* `/digital-deception/rspan/api/result`: The API endpoint that uploads the initial test data to the server which correlates all user data to one record. All API endpoints require an API key which is configured using the file `/oswald_reading_span/configuration/api.key`.
* `/digital-deception/api/export`: Exports the given test ids to a CSV file and then serves that file up to the client. Requires API key and LDAP login.
Configuration

The application configures specific endpoint details (REST, methods supported, JSON in/out) using cherrypy config files: https://cherrypydocrework.readthedocs.io/config.html. In the span task, these 3 files are responsible for configuring endpoints:
/oswald_reading_span/base_config.py configuration common to both development and production
/oswald_reading_span/development_config.py configuration specific to development mode
/oswald_reading_span/production_config.py configuration specific to production mode

* NOTE: Currently, when running in production mode, the main span task does not load content until it receives a Javascript window message from a peer (Qualtrics in our case) with a randomized order for the feed data. For more information, see the Qualtrics section below.
* NOTE: In practice, there is very little difference between production and development configurations, but the distinction is kept should the need for one ever arise. The main difference at this point is that a MySQL server connection will be used in production mode, instead of a SQLite file.
* NOTE: Mounting this application specific configuration to every url endpoint in cherrypy comes with some unpleasant side-effects. Namely, the static file urls all get mounted to every sub-url, so there are multiple endpoints that host the same static content. This doesn’t degrade performance, or cause any issues, but is noted here should issues arise. Consult the cherrypy documentation on configuration for information on the proper way to configure endpoints.

## Domain Name
In the server architecture the experiment was originally hosted on, multiple unrelated servers were hosted under the same domain name. To account for this, the Span Task uses an assumed subdomain of /digital-deception/rspan for all urls on the server. You can adjust this to fit your needs by setting the subdomain parameter when running application.py (i.e. pass just / to use no subdomain). You can also adjust the server port, which is 8080 by default in the same way.

## Filesystem
The server application uses a few different filesystem paths at runtime in order to ensure it has access to all the requisite files. These paths are outlined below:
* `server_directory`: This path should point to the root of the git repository code on the machine. This should be discovered automatically using the python builtin __file__ variable.
* `template_location`: This path should point to /oswald_reading_span/frontend/templates and contains all the jinja2 templates that are rendered by Cherrypy. This should be automatically discovered at runtime.
* `shared_data_directory`: This is an implementation specific detail of the server architecture the experiments were originally run on. The span task does not specifically read or write any files to this directory. It can be safely ignored, but may be used as a data directory for any purpose.

# Frontend
## Overview
The frontend of the application is developed using ReactJS, webpack and npm. To debug the frontend using npm, you can run npm run start-experiment from within the `/oswald_reading_span/frontend/span` task folder. Note that in the current setup, images are hosted statically by Cherrypy and will not show up.

The frontend is broken up into 2 different main files, `experiment.js` and `dashboard.js`. The `package.json` file handles building the appropriate file based on the command run, start-experiment or start-dashboard.
Outline
Provided here is a rough outline of the frontend source code. Files not mentioned here are either not in use, extremely specific, or are simply used by another piece outlined here.

The frontend code relies heavily on the Bloc design pattern which makes managing a complex app with many events and transitions easy. Blocs maintain a current state, which is emitted to BlocBuilders as a stream whenever that state changes. Blocs react to Events and transition states accordingly.

The frontend code is broken up into 3 sub projects written in ReactJS: common, export, main. The common project contains small utility functions and common javascript logic used by both the export and main projects (primarily, networking code). The export project contains the code to draw the data export table, and send network requests to the backend to export the data to CSV. The main project is the meat of the code, and is described by this outline:
Index.js: The entry point to the application. Handled here are the Window.postMessage events for embedding in Qualtrics, and rendering the main React component in App.tsx.
App.tsx: The main React component of the experiment. This uses AppBloc.ts and a BlocBuilder to render the main screens of the experiment based on the current AppState.
/states/: Contains definitions of the different states of the app, practice letters session, practice sentence session, practice both session, and main experiment session. These files can be viewed as defining a map of the transitions of the app throughout the lifetime of the task. They are each tied to a Bloc which maps Events to state transitions.
/events/: Linked to states, contains event definitions that indicate the many different events that the app responds to. Each event is generally tied to one of the Blocs, and is tied to a transition from one state to another. Some events are directly tied to user input, while others are generated programmatically to orchestrate the experiment timing.
/stimuli/: Contains the stimuli used by the experiment, primarily a bank of sentences and letters. This information is pulled directly from the original E-Prime experiment.
/letters/: Contains experiment information pertaining to letters, including the PracticeLetters Bloc and components for Letter instructions, Letter View and Letter Grid View.
/sentence/: Contains experiment information pertaining to sentences, including the PracticeSentences Bloc and components for Sentence instructions, Sentence View and Sentence Feedback View.
/experiment/: Contains experiment information orchestrating the practice both session and the main session, including the Experiment Bloc and components for the Practice Both instructions.
/assets/instructions/: Screenshots of the experiment used in the instruction screens to demonstrate the functioning of the task.
Docker
The docker image is built on top of the CherrypyDocker image: https://github.com/iandavis0527/CherrypyDocker. You should build and tag this image by cloning the repo and running python build_docker_container.py first.

If you build and run the docker container here using build_docker_container.py, the server will run by default on port 5001. This is an implementation detail of the server architecture of the original experiment. You can change this by editing build_docker_container.py or building your own docker deploy script.

NOTE: Cherrypy is classed as a production ready http server by itself, which is what these docker images use. However, cherrypy supports being run as a WSGI application using mod-wsgi with most common web servers.
Result Data
Structure definitions for result data are contained both in the frontend and backend code. In the frontend, they are located in /common/src/network/serialized_data/. In the backend, you can find them in /models/. There are some asymmetries between the two implementations, mainly due to SQL database structure requirements.

A loose overview of the result data structure (defined in the frontend) is as follows:

Result 
subjectId: string
experimentVersion: string
timestamp: unix timestamp
letter_result: LetterResult
sentence_result: SentenceResult
LetterResult
proper_letters: Array<Array<String>>
chosen_letters: Array<Array<String>>
number_correct: number
total_letters: number
SentenceResult
sentences: Array<String>
responses: Array<boolean | null> // Can be null in the case that the user didn’t respond within the maximum reading time.
expected_response: Array<boolean>
reading_times: Array<number | null> // Can be null in the case that the user didn’t respond within the maximum reading time.
average_rt_millis: number
number_correct: number
speed_errors: number
NOTE: Network storage of results was not tested on low-bandwidth connections like cellular. There is currently no robust retry logic in the code for uploading results, so if a network error occurs causing timeout or other issue, the results will not be uploaded.
Database
The span task uses SQLAlchemy for database management, so most common SQL backends are supported (MySQL, PostreSQL, SQLite, etc). By default, the application has support for SQLite and MySQL, and determines which to use based on the production flag passed to the server and the existence of a mysql.credentials file, describing the connection to the MySQL Server. This file should be a single JSON object with keys username, password, host, db_name and live in /oswald_reading_span/backend/configuration/. 

SQLAlchemy table and record definitions are organized throughout the backend folder, in files named models.py. 

Initialization of the SQLAlchemy models and the connection to the database are done within /oswald_reading_span/application.py:setup_server. The server uses the class SQLAlchemyPlugin from CherrypyUtils to handle interoperability between Cherrypy and SQLAlchemy. At a high level, this tool makes a SQLAlchemy session available for all configured cherrypy requests under cherrypy.requests.databases[“oswald_reading”]. 

To configure an endpoint to use SQLAlchemy sessions, enable the tool in configuration: “tools.oswald_reading_database.on”: True. Examples of this can be seen in /oswald_reading_span/backend/configuration/base_config.py.
Qualtrics
The experiment is currently designed to be embedded within a Qualtrics survey. To do this, it uses the Javascript Window.postMessage() function: https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage. Within Qualtrics, the span task would be embedded on a page as an iframe. The span task checks for the existence of a parent window/frame as evidence that it is embedded within a survey. The messaging between Qualtrics and the span task can be described as follows:

Qualtrics navigates to the question with the span task iframe and runs a javascript addon to initialize the page and disable the next button contingent on the span task section finishing. 
The user finishes the span task, and the span task sends a window message to qualtrics indicating the task is finished.
Qualtrics receives the task finished message and re-enables the next button.

To see more details on the embed interface that powers the Qualtrics side of the steps above, review the scripts in /scripts/, primarily: span task-embed-interface.js. Most of the span task messaging is handled within /frontend/main/src/index.js.
NOTE: This embed interface is not tied in any way to Qualtrics, and could be adapted to any survey engine that supports adding custom Javascript to a question (e.x. LimeSurvey).

