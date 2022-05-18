import React from "react";
import "../css/instructions.css";
import InstructionsPage from "../components/InstructionsPage";
import { LetterInstructions1ClickedEvent } from "../events/InstructionsEvents";
import package_data from "../../package.json";

export default class LetterInstructions1 extends React.Component {
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
          "In this portion of the experiment, you will work on memorizing letters shown on the screen in conjunction with reading and interpreting sentences.",
          "At the start, you will complete some practice sessions to get familiar with how the task works.",
          <span className={"version-number-block"}>
            Current Version: {package_data.version}
          </span>,
        ]}
      />
    );
  }

  onInstructionsClicked() {
    this.props.bloc.add(new LetterInstructions1ClickedEvent());
  }
}
