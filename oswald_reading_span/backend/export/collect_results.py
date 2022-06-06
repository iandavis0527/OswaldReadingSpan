from typing import Iterable
from sqlalchemy.sql import text
from sqlalchemy.sql import bindparam
from oswald_reading_span.backend.models.letter_response import ReadingSpanLetterResponse

from oswald_reading_span.backend.models.result import ReadingSpanResult
from oswald_reading_span.backend.models.sentence_response import ReadingSpanSentenceResponse
from oswald_reading_span.backend.models.sentences import ReadingSpanSentence


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
    data = []
    results = session.query(ReadingSpanResult).filter(ReadingSpanResult.subject_id.in_(subject_ids))

    for result in results:
        letter_responses = (
            session.query(ReadingSpanLetterResponse).filter(ReadingSpanLetterResponse.test_id == result.id).all()
        )
        sentence_responses = (
            session.query(ReadingSpanSentenceResponse).filter(ReadingSpanSentenceResponse.test_id == result.id).all()
        )

        total_letters = letter_responses[0].total_letters
        total_correct_letters = letter_responses[0].number_correct
        total_sentences = len(sentence_responses)
        total_sentences_correct = 0
        average_reading_time = 0
        speed_errors = 0

        for sentence in sentence_responses:
            sentence_data = (
                session.query(ReadingSpanSentence).filter(ReadingSpanSentence.id == sentence.sentence_id).all()
            )[0]

            if sentence.response == sentence_data.expected_response:
                total_sentences_correct += 1

            if sentence.reading_time:
                average_reading_time += sentence.reading_time

            if sentence.speed_error:
                speed_errors += 1

        average_reading_time = average_reading_time / total_sentences

        data.append(
            [
                result.id,
                result.timestamp,
                result.subject_id,
                result.experiment_version,
                total_correct_letters,
                total_letters,
                total_sentences_correct,
                total_sentences,
                average_reading_time,
                speed_errors,
            ]
        )

    return data


def collect_long_results(session, subject_ids: Iterable[str]) -> Iterable[dict]:
    data = []
    results = session.query(ReadingSpanResult).filter(ReadingSpanResult.subject_id.in_(subject_ids))

    for result in results:
        letter_responses = (
            session.query(ReadingSpanLetterResponse).filter(ReadingSpanLetterResponse.test_id == result.id).all()
        )
        sentence_responses = (
            session.query(ReadingSpanSentenceResponse).filter(ReadingSpanSentenceResponse.test_id == result.id).all()
        )

        current_sentence_offset = 0

        for letter_response in letter_responses:
            for (chosen_letter, proper_letter) in zip(
                letter_response.chosen_letters.split(","),
                letter_response.proper_letters.split(","),
            ):
                if current_sentence_offset >= len(sentence_responses):
                    print("using N/A sentence because we are past the limit of sentences")
                    sentence = "N/A"
                    expected_response = "N/A"
                    response = "N/A"
                    reading_time = "N/A"
                    speed_error = "N/A"
                else:
                    current_sentence = sentence_responses[current_sentence_offset]
                    current_sentence_data = (
                        session.query(ReadingSpanSentence)
                        .filter(ReadingSpanSentence.id == current_sentence.sentence_id)
                        .all()
                    )[0]
                    current_sentence_offset += 1
                    sentence = current_sentence_data.sentence
                    expected_response = current_sentence_data.expected_response
                    response = current_sentence.response
                    reading_time = current_sentence.reading_time
                    speed_error = current_sentence.speed_error

                data.append(
                    [
                        result.id,
                        result.timestamp,
                        result.subject_id,
                        result.experiment_version,
                        chosen_letter,
                        proper_letter,
                        sentence,
                        response,
                        expected_response,
                        reading_time,
                        speed_error,
                    ]
                )

        if current_sentence_offset < len(sentence_responses):
            print("parsing left over sentences after finishing all letter responses")

            for current_sentence in sentence_responses[current_sentence_offset:]:
                current_sentence_data = (
                    session.query(ReadingSpanSentence)
                    .filter(ReadingSpanSentence.id == current_sentence.sentence_id)
                    .all()
                )[0]
                sentence = current_sentence_data.sentence
                expected_response = current_sentence_data.expected_response
                response = current_sentence.response
                reading_time = current_sentence.reading_time if current_sentence.reading_time else "N/A"
                speed_error = current_sentence.speed_error if current_sentence.speed_error is not None else "N/A"

                data.append(
                    [
                        result.id,
                        result.timestamp,
                        result.subject_id,
                        result.experiment_version,
                        "N/A",
                        "N/A",
                        sentence,
                        response,
                        expected_response,
                        reading_time,
                        speed_error,
                    ]
                )

    return data


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
        "speed_errors",
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
        "sentence_read_time",
        "speed_error",
    ]
