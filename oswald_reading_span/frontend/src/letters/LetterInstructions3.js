import React from "react";
import InstructionsPage from "../components/InstructionsPage";
import image from "../assets/instructions/instructions-letter-grid1.png";
import { LetterInstructions3ClickedEvent } from "../events/InstructionsEvents";

export default class LetterInstructions3 extends React.Component {
  constructor(props) {
    super(props);

    this.onInstructionsClicked = this.onInstructionsClicked.bind(this);
  }

  render() {
    return (
      <InstructionsPage
        onInstructionsClicked={this.onInstructionsClicked}
        continuePrompt={"Click in this box to continue."}
        title={""}
        paragraphs={[
          <span>
            After the set of letters has been shown, you will see a screen
            listing 12 possible letters.
          </span>,
          <span>
            Your job is to select all letters from the set in the{" "}
            <b>same order</b> they were presented. To do this, use the mouse to
            click on the letters. The letters selected will appear at the bottom
            of the screen
          </span>,
          <img src={image} className={"instruction-image"} />,
        ]}
      />
    );
  }

  onInstructionsClicked() {
    this.props.bloc.add(new LetterInstructions3ClickedEvent());
  }
}
