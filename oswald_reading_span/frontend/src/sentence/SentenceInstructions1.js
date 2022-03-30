import React from "react";
import InstructionsPage from "../components/InstructionsPage";
import { SentenceInstructions1ClickedEvent } from "../events/InstructionsEvents";

export default class SentenceInstructions1 extends React.Component {
  constructor(props) {
    super(props);

    this.onInstructionsClicked = this.onInstructionsClicked.bind(this);
  }

  render() {
    return (
      <InstructionsPage
        onInstructionsClicked={this.onInstructionsClicked}
        continuePrompt={"Click in this box to continue."}
        title={"INSTRUCTIONS"}
        paragraphs={[
          <span>
            Now you will practice the sentence reading part of the task.
          </span>,
          <span>A sentence will appear on the screen like this:</span>,
          <span className={"instruction-sentence-preview"}>
            I like to run in the park with my trees on upside down.
          </span>,
          <span>
            When you read the sentence, determine whether it makes sense.{" "}
          </span>,
          <span>For example, the sentence does not make sense.</span>,
          <span>
            Once you have decided, click the mouse anywhere to continue.
          </span>,
        ]}
      />
    );
  }

  onInstructionsClicked() {
    this.props.bloc.add(new SentenceInstructions1ClickedEvent());
  }
}
