from typing import Dict, Iterable
from sqlalchemy import Column, DATETIME, Text, String

from cherrypy_utils import timestamp_utils
from cherrypy_utils.database import Base, BaseEventRecord

from oswald_reading_span.backend.models.letter_response import ReadingSpanLetterResponse
from oswald_reading_span.backend.models.sentence_response import ReadingSpanSentenceResponse
from oswald_reading_span.backend.models.sentences import ReadingSpanSentence


class MappedReadingSpanResult:
    def __init__(self, id, subject_id, emulator_version, timestamp):
        self.id = id
        self.subject_id = subject_id
        self.emulator_version = emulator_version
        self.timestamp = timestamp
        self.sentence_responses = []  # type: Iterable[Iterable[ReadingSpanSentenceResponse, ReadingSpanSentence]]
        self.letter_responses = []  # type: Iterable[ReadingSpanLetterResponse]


class ReadingSpanResult(Base, BaseEventRecord):
    __tablename__ = "ReadingSpanResult"

    timestamp = Column(
        DATETIME(timezone=True),
        nullable=False,
        server_default=timestamp_utils.default_timestamp().isoformat(),
    )
    subject_id = Column(Text, nullable=False)
    experiment_version = Column(String(512), server_default="1.0.0", nullable=False)

    @classmethod
    def _parse_dict(cls, data: Dict) -> Dict:
        return timestamp_utils.convert_dictionary_keys(
            data,
            [
                "timestamp",
            ],
        )

    def _to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "experiment_version": self.experiment_version,
            "subject_id": self.subject_id,
        }


def get_reading_span_sentence_results(session):
    return (
        MappedReadingSpanResult(
            entity.id,
            entity.subject_id,
            entity.experiment_version,
            entity.timestamp,
        )
        for entity in (
            session.query(ReadingSpanSentenceResponse)
            .join(
                ReadingSpanResult,
                ReadingSpanResult.id == ReadingSpanSentenceResponse.test_id,
            )
            .join(
                ReadingSpanSentence,
                ReadingSpanSentenceResponse.sentence_id == ReadingSpanSentence.id,
            )
            .join(
                ReadingSpanLetterResponse,
                ReadingSpanResult.id == ReadingSpanLetterResponse.test_id,
            )
        ).all()
    )
