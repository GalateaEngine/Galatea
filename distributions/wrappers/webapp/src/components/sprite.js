import React, { Component } from "react";

export default class Sprite extends Component {
  constructor(props) {
    super(props);
    this.state = { emotion: "" };
  }

  render() {
    return (
      <div
        style={{
          height: "100%",
          width: "100%",
          position: "absoulte",
          bottom: 0,
          textAlign: "center"
        }}
      >
        <img
          className="sprite"
          style={{
            height: "100vh",
            bottom: 0,
            opacity: "0.95"
          }}
          alt="sprite"
          src={require("./sprites/" + this.props.emotion + ".png")}
        />
      </div>
    );
  }
}
