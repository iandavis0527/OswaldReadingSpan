import { filter, std } from 'mathjs';
import filterNulls from '../utils/filter_nulls';

export class SentenceResult {
    public sentences: Array<String> = [];
    public responses: Array<boolean | null> = [];
    public expectedResponses: Array<boolean> = [];
    public readingTimes: Array<number | null> = [];
    public averageRTMillis: number = 0;
    public numberCorrect: number = 0;
    public speedErrors: number = 0;

    addInput(sentence: String, response: boolean | null, expectedResponse: boolean, readTimeMillis: number | null) {
        this.sentences.push(sentence);
        this.responses.push(response);
        this.expectedResponses.push(expectedResponse);
        this.readingTimes.push(readTimeMillis);

        if (response === null) this.speedErrors++;

        if (response === expectedResponse) {
            this.numberCorrect++;
        } else {
            console.debug("You got this one wrong");
            console.debug(sentence);
        }

        if (this.averageRTMillis === 0 && readTimeMillis !== null) {
            this.averageRTMillis = readTimeMillis;
        } else if (readTimeMillis !== null) {
            this.averageRTMillis = (this.averageRTMillis + readTimeMillis) / 2;
        }
    }

    percentCorrect(): number {
        console.debug("numberCorrect: " + this.numberCorrect);
        console.debug("total sentences: " + this.sentences.length);
        return (this.numberCorrect / this.sentences.length) * 100;
    }

    meanReadTime(): number {
        let sum = 0;

        for (let i = 0; i < this.readingTimes.length; i++) {
            let readingTime = this.readingTimes[i];
            if (readingTime === null) continue;

            sum += readingTime;
        }

        return sum / this.readingTimes.length;
    }

    maxReadingTime(): number {
        const stdDeviation = std(filterNulls(this.readingTimes));
        console.debug(`[SENTENCE_PRACTICE][SENTENCE_MAX] - AVERAGE READING TIME = ${this.meanReadTime()}`);
        console.debug(`[SENTENCE_PRACTICE][SENTENCE_MAX] - STANDARD DEVIATION = ${stdDeviation}`);
        // The max reading time is defined as 2.5 times the standard deviation of the reading times.
        return this.meanReadTime() + (2.5 * stdDeviation);
    }
}
