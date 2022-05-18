import React from "react";
import InstructionsPage from "../components/InstructionsPage";
import { SentencePracticeStartedEvent } from "../events/SentenceEvents";

export default class SentenceInstructions4 extends React.Component {
  constructor(props) {
    super(props);

    this.onInstructionsClicked = this.onInstructionsClicked.bind(this);
  }

  render() {
    return (
      <InstructionsPage
        onInstructionsClicked={this.onInstructionsClicked}
        continuePrompt={"Click in this box to continue."}
        paragraphs={[
          <span>
            It is very important that you try to read the sentences as{" "}
            <b>QUICKLY</b> and answer as <b>ACCURATELY</b> as possible.
          </span>,
          <span>
            Your reading times during the practice will be used to determine the
            pace at which sentences are displayed for the remainder of the task.
          </span>,
        ]}
      />
    );
  }

  onInstructionsClicked() {
    this.props.bloc.add(new SentencePracticeStartedEvent());
  }
}
