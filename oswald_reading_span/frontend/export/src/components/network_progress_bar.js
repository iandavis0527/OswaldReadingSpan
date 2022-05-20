import React from "react";
import CircularIndeterminate from "./circular_indeterminate_progress";

import "./network_progress_bar.css";

export default class NetworkProgressBar extends React.Component {
  constructor(props) {
    super(props);

    this.progressBarRef = React.createRef();
    this.progressBar = null;

    this.state = {
      data: null,
      dataLoaded: false,
    };
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (this.state.dataLoaded && !prevState.dataLoaded) {
      this.props.onDataLoaded(this.state.data);
    }
  }

  componentDidMount() {
    this.props.initiateDataLoad().then((data) => {
      this.setState({
        data: data,
        dataLoaded: true,
      });
    });
  }

  render() {
    if (this.state.dataLoaded) {
      return "";
    }

    return (
      <div className={"network-progress-bar"}>
        <CircularIndeterminate />
      </div>
    );
  }
}
