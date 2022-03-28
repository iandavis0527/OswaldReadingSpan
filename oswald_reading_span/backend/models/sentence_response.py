from typing import Dict, Iterable, List
from sqlalchemy import Column, Integer, Boolean

from cherrypy_utils.database import Base, BaseEventRecord

from oswald_reading_span.backend.models.sentences import ReadingSpanSentence


class ReadingSpanSentenceResponse(Base, BaseEventRecord):
    __tablename__ = "ReadingSpanSentenceResponse"

    test_id = Column(Integer, nullable=False)
    sentence_id = Column(Integer, nullable=False)
    response = Column(Boolean, nullable=True)
    reading_time = Column(Integer, nullable=True)
    speed_error = Column(Boolean, nullable=False)

    @classmethod
    def _parse_dict(cls, data: Dict) -> Dict:
        return data

    def _to_dict(self, *_, **__):
        return {
            "test_id": self.test_id,
            "sentence_id": self.sentence_id,
            "response": self.response,
        }


def get_sentence_responses(session, test_id) -> Iterable:
    return (
        session.query(ReadingSpanSentenceResponse)
        .join(ReadingSpanSentence, ReadingSpanSentenceResponse.sentence_id == ReadingSpanSentence.id)
        .filter(ReadingSpanSentenceResponse.test_id == test_id)
        .all()
    )
