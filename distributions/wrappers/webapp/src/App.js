import React, { Component } from "react";
import Chatbox from "./components/chatbox";

import Sprite from "./components/sprite";

import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { emotion: "worry" };
    this.changePic = this.changePic.bind(this);
  }

  changePic(e) {
    this.setState({ emotion: e });
  }
  render() {
    return (
      <div className="App">
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, width=device-width"
        />
        <div className="background"></div>

        <Sprite emotion={this.state.emotion} />
        <Chatbox style={{}} changePic={e => this.changePic(e)} />
      </div>
    );
  }
}

export default App;
