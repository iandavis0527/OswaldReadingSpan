import React from "react";
import InstructionsPage from "../components/InstructionsPage";
import { SentencePracticeStartedEvent } from "../events/SentenceEvents";
import image from "../assets/instructions/instructions-sentence-feedback.png";
import { SentenceInstructions3ClickedEvent } from "../events/InstructionsEvents";

export default class SentenceInstructions3 extends React.Component {
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
            After clicking on either the{" "}
            <span className={"orange-instruction-text"}>TRUE</span> or{" "}
            <span className={"purple-instruction-text"}>FALSE</span> button, a
            message will appear indicating whether you made a correct or
            incorrect choice.
          </span>,
          <span>
            Once you have read the feedback, click the{" "}
            <span className={"green-instruction-text"}>NEXT</span> button to
            continue.
          </span>,
          <img src={image} className={"instruction-image"} />,
        ]}
      />
    );
  }

  onInstructionsClicked() {
    this.props.bloc.add(new SentenceInstructions3ClickedEvent());
  }
}
