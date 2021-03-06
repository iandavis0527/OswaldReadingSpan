import {SetFinishedEvent} from "../events/ExperimentEvent";

export enum ExperimentStateType {
    LETTER_INSTRUCTIONS1,
    LETTER_INSTRUCTIONS2,
    LETTER_INSTRUCTIONS3,
    LETTER_INSTRUCTIONS4,
    SENTENCE_INSTRUCTIONS1,
    SENTENCE_INSTRUCTIONS2,
    SENTENCE_INSTRUCTIONS3,
    SENTENCE_INSTRUCTIONS4,
    COMBINED_INSTRUCTIONS1,
    COMBINED_INSTRUCTIONS2,
    COMBINED_INSTRUCTIONS3,
    EXPERIMENT_START_SCREEN,
    SHOWING_SENTENCE,
    SHOWING_SENSE_PROMPT,
    SHOWING_LETTER,
    SENTENCE_FEEDBACK,
    HIDING_LETTER,
    SHOWING_GRID,
    SHOWING_LETTER_PRACTICE_FEEDBACK,
    ISI_DELAY,
    SET_FEEDBACK,
}

export abstract class ExperimentState {
    readonly stateType: ExperimentStateType;

    protected constructor(stateType: ExperimentStateType) {
        this.stateType = stateType;
    }
}

export class ISIDelayState extends ExperimentState {
    constructor() {
        super(ExperimentStateType.ISI_DELAY);
    }
}

export class SetFeedbackState extends ExperimentState {
    readonly percentCorrect: number;
    readonly sentencesCorrect: number;
    readonly totalSentences: number;
    readonly setSize: number;
    readonly lettersCorrect: number;

    constructor(event: SetFinishedEvent) {
        super(ExperimentStateType.SET_FEEDBACK);
        this.setSize = event.setSize;
        this.sentencesCorrect = event.sentencesCorrect;
        this.totalSentences = event.totalSentences;
        this.lettersCorrect = event.lettersCorrect;
        this.percentCorrect = event.percentCorrect;
    }
}