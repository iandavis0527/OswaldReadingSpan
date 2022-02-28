import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from cherrypy_utils.database import Base

from oswald_reading_span.backend.export import collect_results

from expected_data import EXPECTED_LONG_FORM

db_filepath = pathlib.Path(__file__).parent.absolute().joinpath("sample_result.db")
connection_string = "sqlite:///{db_hostname_filename}".format(db_hostname_filename=db_filepath)

engine = create_engine(connection_string)
Base.metadata.create_all(engine)
session = Session(engine)

result = collect_results.collect_results_summary(session, ["missing-subject-id"]).first()

assert result is not None
assert result == (1, "2022-02-17 20:28:06.553000", "missing-subject-id", "0.1.0", 28, 30, 23, 30, 2820.233333333333)

results = collect_results.collect_long_results(session, ["missing-subject-id"]).all()

assert results is not None
assert results == EXPECTED_LONG_FORM
