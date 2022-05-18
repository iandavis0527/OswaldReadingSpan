import { ExperimentBloc } from "./ExperimentBloc";

test("ensure no repeats between practice both and main experiment", () => {
  const bloc = new ExperimentBloc(null);
  bloc.generatePracticeSets();
  const practiceSentences = bloc.sentenceSets.flat();
  bloc.generateExperimentSets();
  const experimentSentences = bloc.sentenceSets.flat();
  for (let i = 0; i < practiceSentences.length; i++) {
    const practiceSentence = practiceSentences[i];
    expect(experimentSentences).not.toEqual(
      expect.arrayContaining([expect.objectContaining(practiceSentence)])
    );
  }
});
