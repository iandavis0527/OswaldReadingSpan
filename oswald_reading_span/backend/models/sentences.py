from typing import Dict
from sqlalchemy import Column, Text, Boolean

from cherrypy_utils.database import Base, BaseEventRecord

from oswald_reading_span.backend.stimuli.sentences import SENTENCES


class ReadingSpanSentence(Base, BaseEventRecord):
    __tablename__ = "ReadingSpanSentence"

    sentence = Column(Text, nullable=False)
    expected_response = Column(Boolean, nullable=False)

    @staticmethod
    def initialize_sentences(session):
        if session.query(ReadingSpanSentence).count() > 0:
            return

        for sentence_data in SENTENCES:
            session.add(
                ReadingSpanSentence(
                    sentence=sentence_data["sentence"],
                    expected_response=sentence_data["expected_response"],
                )
            )

        session.flush()

    @classmethod
    def _parse_dict(cls, data: Dict) -> Dict:
        return data

    def _to_dict(self, *_, **__):
        return {
            "sentence": self.sentence,
            "expected_response": self.expected_response,
        }
