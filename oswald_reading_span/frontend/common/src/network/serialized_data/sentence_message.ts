import { SentenceResult } from "../../results/SentenceResult";

export interface SerializedSentenceMessage {
    sentences: Array<String>;
    responses: Array<boolean | null>;
    expected_responses: Array<boolean>;
    reading_times: Array<number | null>;
    average_rt_millis: number;
    number_correct: number;
    speed_errors: number;
}

export function serializeSentenceResult(result: SentenceResult): SerializedSentenceMessage {
    return {
        sentences: result.sentences,
        responses: result.responses,
        expected_responses: result.expectedResponses,
        reading_times: result.readingTimes,
        average_rt_millis: result.averageRTMillis,
        number_correct: result.numberCorrect,
        speed_errors: result.speedErrors,
    };
}

export function deserializeSentenceResult(result: SerializedSentenceMessage): SentenceResult {
    const sentenceResult = new SentenceResult();
    sentenceResult.sentences = result.sentences;
    sentenceResult.responses = result.responses;
    sentenceResult.expectedResponses = result.expected_responses;
    sentenceResult.readingTimes = result.reading_times;
    sentenceResult.averageRTMillis = result.average_rt_millis;
    sentenceResult.numberCorrect = result.number_correct;
    sentenceResult.speedErrors = result.speed_errors;
    return sentenceResult;
}
