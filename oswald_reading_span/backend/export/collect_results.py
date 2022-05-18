import datetime
from typing import Iterable
from sqlalchemy.sql import text
from oswald_reading_span.backend.models.letter_response import ReadingSpanLetterResponse

from oswald_reading_span.backend.models.result import ReadingSpanResult
from oswald_reading_span.backend.models.sentence_response import ReadingSpanSentenceResponse
from oswald_reading_span.backend.models.sentences import ReadingSpanSentence


SUMMARY_QUERY = text(
    """
SELECT DISTINCT
    ReadingSpanResult.id, timestamp, subject_id, experiment_version,
    number_correct AS number_letters_correct, total_letters,
    (SELECT 
        COUNT(*)
        FROM ReadingSpanSentenceResponse 
            INNER JOIN ReadingSpanSentence
            ON ReadingSpanSentenceResponse.sentence_id = ReadingSpanSentence.id
        WHERE ReadingSpanResult.id = ReadingSpanSentenceResponse.test_id 
        AND ReadingSpanSentenceResponse.response = ReadingSpanSentence.expected_response
    ) AS correct_sentence_count,
    (SELECT 
        COUNT(*) 
        FROM ReadingSpanSentenceResponse
            INNER JOIN ReadingSpanSentence
            ON ReadingSpanSentenceResponse.sentence_id = ReadingSpanSentence.id
        WHERE ReadingSpanResult.id = ReadingSpanSentenceResponse.test_id
    ) AS total_sentence_count,
    (SELECT 
        AVG(ReadingSpanSentenceResponse.reading_time) 
        FROM ReadingSpanSentenceResponse
        WHERE ReadingSpanResult.id = ReadingSpanSentenceResponse.test_id
    ) AS average_sentence_read_time
    FROM ReadingSpanResult
    INNER JOIN ReadingSpanSentenceResponse
        ON ReadingSpanResult.id = ReadingSpanSentenceResponse.test_id 
    INNER JOIN ReadingSpanSentence 
        ON ReadingSpanSentenceResponse.sentence_id = ReadingSpanSentence.id 
    INNER JOIN ReadingSpanLetterResponse
        ON ReadingSpanResult.id = ReadingSpanLetterResponse.test_id
    WHERE ReadingSpanResult.subject_id IN (:subject_ids);
"""
)

LONG_FORM_QUERY = text(
    """
SELECT DISTINCT
    ReadingSpanResult.id, timestamp, subject_id, experiment_version,
    chosen_letters, proper_letters,
    sentence, response AS sentence_response, expected_response AS expected_sentence_response
    FROM ReadingSpanResult
    INNER JOIN ReadingSpanSentenceResponse
        ON ReadingSpanResult.id = ReadingSpanSentenceResponse.test_id 
    INNER JOIN ReadingSpanSentence 
        ON ReadingSpanSentenceResponse.sentence_id = ReadingSpanSentence.id 
    INNER JOIN ReadingSpanLetterResponse 
        ON ReadingSpanResult.id = ReadingSpanLetterResponse.test_id
    WHERE ReadingSpanResult.subject_id IN (:subject_ids);
"""
)


def collect_results_summary(session, subject_ids: Iterable[str]) -> Iterable[dict]:
    query = SUMMARY_QUERY.bindparams(subject_ids=",".join(subject_ids))
    return session.execute(query)


def collect_long_results(session, subject_ids: Iterable[str]) -> Iterable[dict]:
    return session.execute(LONG_FORM_QUERY.bindparams(subject_ids=",".join(subject_ids)))


def summary_header():
    return [
        "id",
        "timestamp",
        "subject_id",
        "experiment_version",
        "number_letters_correct",
        "total_letters",
    ]


def long_header():
    return [
        "id",
        "timestamp",
        "subject_id",
        "experiment_version",
        "chosen_letters",
        "proper_letters",
        "sentence",
        "sentence_response",
        "expected_sentence_response",
    ]
