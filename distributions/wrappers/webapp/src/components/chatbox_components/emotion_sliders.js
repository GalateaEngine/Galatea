import React, { Component } from "react";

export default class Emotion_slider extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.props.return({ [this.props.emotion]: (event / 100).toString() });
  }

  render() {
    return (
      <div
        style={{
          display: "inline-block",
          padding: "0.1%",
          textTransform: "capitalize"
        }}
      >
        {this.props.emotion}
        <br />
        <input
          style={{ width: "75px" }}
          type="range"
          max={100}
          step={0.1}
          onChange={evt => {
            this.handleChange(evt.target.value);
          }}
        />
        <div />
      </div>
    );
  }
}
