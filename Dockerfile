FROM cherrypy:latest

ENV PYTHONPATH "${PYTHONPATH}:/OswaldReadingSpan/"

WORKDIR /OswaldReadingSpan/

COPY ./oswald_reading_span/frontend/common /OswaldReadingSpan/oswald_reading_span/frontend/common

WORKDIR /OswaldReadingSpan/oswald_reading_span/frontend/common

RUN npm install --production
RUN npm run build

COPY ./oswald_reading_span/frontend/export /OswaldReadingSpan/oswald_reading_span/frontend/export

WORKDIR /OswaldReadingSpan/oswald_reading_span/frontend/export

RUN npm install --production
RUN npm run build

COPY ./oswald_reading_span/frontend/main /OswaldReadingSpan/oswald_reading_span/frontend/main

WORKDIR /OswaldReadingSpan/oswald_reading_span/frontend/main

RUN npm install --production
RUN npm run build

WORKDIR /OswaldReadingSpan/

COPY ./requirements.txt /OswaldReadingSpan/

RUN pip3 install -r requirements.txt

COPY ./oswald_reading_span/__init__.py /OswaldReadingSpan/oswald_reading_span
COPY ./oswald_reading_span/application.py /OswaldReadingSpan/oswald_reading_span
COPY ./oswald_reading_span/backend /OswaldReadingSpan/oswald_reading_span/backend

EXPOSE 5002

CMD ["python3.6", "-m", "oswald_reading_span.application", "--shared_data_location", "/oswald_reading_data/", "--port", "5002", "--subdomain", "/digital-deception/rspan/", "--production"]
