import React from "react";
import autoBind from "auto-bind";

import ExportScreen from "./screens/ExportScreen";
import LoginScreen from "./screens/LoginScreen";

import "./App.css";

class AppState {
  static LoggingIn = new AppState("loggingIn");
  static ExportingData = new AppState("exportingData");

  constructor(name) {
    this.name = name;
  }
}

class App extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);
    this.state = {
      currentState: AppState.LoggingIn,
    };
  }

  render() {
    switch (this.state.currentState) {
      case AppState.LoggingIn:
      default:
        return (
          <div className="App">
            <LoginScreen onLoginSucceeded={this.onLoginSucceeded} />
          </div>
        );
      case AppState.ExportingData:
        return (
          <div className="App">
            <ExportScreen />
          </div>
        );
    }
  }

  onLoginSucceeded() {
    this.setState({ currentState: AppState.ExportingData });
  }
}

export default App;
