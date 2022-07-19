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

Once all dependencies are prepared, you can run the span task using python -m oswald_reading_span.application. You should see output similar to:
```
    [07/Jul/2022:11:16:17] ENGINE Bus STARTING
    [07/Jul/2022:11:16:17] ENGINE Serving on http://0.0.0.0:8080
    [07/Jul/2022:11:16:17] ENGINE Bus STARTED
```

You can then navigate your browser to [http://localhost:8080/digital-deception/rspan?subjectId=test123]
