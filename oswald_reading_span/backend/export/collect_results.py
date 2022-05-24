from typing import Iterable
from more_itertools import numeric_range
from sqlalchemy.sql import text
from sqlalchemy.sql import bindparam


SUMMARY_QUERY = text(
    """
SELECT
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
    WHERE ReadingSpanResult.subject_id IN :subject_ids;
"""
)

SUMMARY_QUERY = SUMMARY_QUERY.bindparams(bindparam("subject_ids", expanding=True))

LONG_FORM_QUERY = text(
    """
SELECT
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
    WHERE ReadingSpanResult.subject_id IN :subject_ids;
"""
)

LONG_FORM_QUERY = LONG_FORM_QUERY.bindparams(bindparam("subject_ids", expanding=True))

LONG_FORM_START = text(
    """
SELECT
    ReadingSpanResult.id, ReadingSpanResult.timestamp, ReadingSpanResult.subject_id, ReadingSpanResult.experiment_version, chosen_letters, proper_letters
    FROM ReadingSpanResult
    INNER JOIN ReadingSpanLetterResponse ON ReadingSpanResult.id = ReadingSpanLetterResponse.test_id
    WHERE ReadingSpanResult.subject_id in :subject_ids ORDER BY ReadingSpanLetterResponse.id;
    """
)

LONG_FORM_START = LONG_FORM_START.bindparams(bindparam("subject_ids", expanding=True))


SELECT_N_SENTENCES = text(
    """
SELECT sentence, response AS sentence_response, expected_response AS expected_sentence_response 
    FROM ReadingSpanSentenceResponse 
    INNER JOIN ReadingSpanSentence 
        ON ReadingSpanSentenceResponse.sentence_id = ReadingSpanSentence.id
    WHERE ReadingSpanSentenceResponse.test_id = :test_id
    LIMIT :num_results, :offset;
    """
)

SELECT_N_SENTENCES = SELECT_N_SENTENCES.bindparams(test_id="", num_results=5, offset=0)


def collect_results_summary(session, subject_ids: Iterable[str]) -> Iterable[dict]:
    # query = SUMMARY_QUERY.bindparams(subject_ids=",".join(subject_ids))
    return session.execute(
        SUMMARY_QUERY,
        params={
            "subject_ids": subject_ids,
        },
    )


def collect_long_results(session, subject_ids: Iterable[str]) -> Iterable[dict]:
    # long_form_start = session.execute(LONG_FORM_START.bindparams(subject_ids=",".join(subject_ids)))
    long_form_start = session.execute(
        LONG_FORM_START,
        params={
            "subject_ids": subject_ids,
        },
    )
    results = []
    current_sentence_offset = 0

    for row in long_form_start.all():
        test_id = row["id"]
        proper_letters = row["proper_letters"].split(",")
        chosen_letters = row["chosen_letters"].split(",")
        number_letters = len(proper_letters)
        sentences = session.execute(
            SELECT_N_SENTENCES,
            params={
                "test_id": test_id,
                "num_results": number_letters,
                "offset": current_sentence_offset,
            },
        )
        current_sentence_offset += number_letters

        for chosen_letter, proper_letter, sentence_row in zip(chosen_letters, proper_letters, sentences):
            results.append(
                [
                    test_id,
                    row["timestamp"],
                    row["subject_id"],
                    row["experiment_version"],
                    chosen_letter,
                    proper_letter,
                    sentence_row["sentence"],
                    sentence_row["sentence_response"],
                    sentence_row["expected_sentence_response"],
                ]
            )

    # return session.execute(LONG_FORM_QUERY.bindparams(subject_ids=",".join(subject_ids)))
    return results


def summary_header():
    return [
        "id",
        "timestamp",
        "subject_id",
        "experiment_version",
        "corrent_letter_count",
        "total_letter_count",
        "correct_sentence_count",
        "total_sentence_count",
        "average_sentence_read_time",
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
