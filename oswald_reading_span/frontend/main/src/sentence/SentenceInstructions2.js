import React from "react";
import InstructionsPage from "../components/InstructionsPage";
import { SentenceInstructions2ClickedEvent } from "../events/InstructionsEvents";
import image from "../assets/instructions/instructions-sentence-prompt.png";

export default class SentenceInstructions2 extends React.Component {
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
            You will then see the statement “This sentence makes sense.”
          </span>,
          <span>
            Below that will be three buttons labeled{" "}
            <span className={"orange-instruction-text"}>TRUE</span>,{" "}
            <span className={"purple-instruction-text"}>FALSE</span>, and{" "}
            <span className={"green-instruction-text"}>NEXT</span>.
          </span>,
          <span>
            If the sentence on the previous screen made sense, click on the
            button labeled{" "}
            <span className={"orange-instruction-text"}>TRUE</span>.
          </span>,
          <span>
            If the sentence did not make sense, click on the button labeled{" "}
            <span className={"purple-instruction-text"}>FALSE</span>.
          </span>,
          <img src={image} className={"instruction-image"} />,
        ]}
      />
    );
  }

  onInstructionsClicked() {
    this.props.bloc.add(new SentenceInstructions2ClickedEvent());
  }
}
