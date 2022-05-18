import React from "react";
import InstructionsPage from "../components/InstructionsPage";
import { LetterInstructions2ClickedEvent } from "../events/InstructionsEvents";
import image from "../assets/instructions/instructions-letter-prompt.png";

export default class LetterInstructions2 extends React.Component {
  constructor(props) {
    super(props);

    this.onInstructionsClicked = this.onInstructionsClicked.bind(this);
  }

  render() {
    return (
      <InstructionsPage
        onInstructionsClicked={this.onInstructionsClicked}
        title={""}
        continuePrompt={"Click in this box to continue."}
        paragraphs={[
          "For the first part of the practice, letters will appear on the screen one at a time.",
          <img src={image} className={"instruction-image"} />,
        ]}
      />
    );
  }

  onInstructionsClicked() {
    this.props.bloc.add(new LetterInstructions2ClickedEvent());
  }
}
