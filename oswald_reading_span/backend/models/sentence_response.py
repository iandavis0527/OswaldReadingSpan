from typing import Dict
from sqlalchemy import Column, Integer, Boolean

from cherrypy_utils.database import Base, BaseEventRecord


class ReadingSpanSentenceResponse(Base, BaseEventRecord):
    __tablename__ = "ReadingSpanSentenceResponse"

    test_id = Column(Integer, nullable=False)
    sentence_id = Column(Integer, nullable=False)
    response = Column(Boolean, nullable=False)
    reading_time = Column(Integer, nullable=False)

    @classmethod
    def _parse_dict(cls, data: Dict) -> Dict:
        return data

    def _to_dict(self, *_, **__):
        return {
            "test_id": self.test_id,
            "sentence_id": self.sentence_id,
            "response": self.response,
        }
