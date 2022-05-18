import React from "react";
import InstructionsPage from "../components/InstructionsPage";
import { LetterPracticeStartedEvent } from "../events/LetterEvents";
import image from "../assets/instructions/instructions-letter-grid2.png";

export default class LetterInstructions4 extends React.Component {
  constructor(props) {
    super(props);

    this.onInstructionsClicked = this.onInstructionsClicked.bind(this);
  }

  render() {
    return (
      <InstructionsPage
        onInstructionsClicked={this.onInstructionsClicked}
        continuePrompt={
          "When you're ready, click in this box to start the letter practice."
        }
        title={""}
        paragraphs={[
          <span>
            When you have selected all the letters and they are in the correct
            order, hit the{" "}
            <span className={"green-instruction-text"}>SUBMIT</span> button at
            the bottom of the screen.
          </span>,
          <span>
            If you make a mistake, click on the{" "}
            <span className={"orange-instruction-text"}>CLEAR</span> button to
            start over.
          </span>,
          <span>
            If you forget one of the letters, click the{" "}
            <span className={"purple-instruction-text"}>BLANK</span> button to
            mark a spot for the missing letter.
          </span>,
          <span>
            It is very important to enter the letters in the same order you saw
            them.
          </span>,
          <img src={image} className={"instruction-image"} />,
        ]}
      />
    );
  }

  onInstructionsClicked() {
    this.props.bloc.add(new LetterPracticeStartedEvent());
  }
}
