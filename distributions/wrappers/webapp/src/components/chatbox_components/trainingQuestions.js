import React, { Component } from "react";
import axios from "axios";

import EmotionSlider from "./emotion_sliders";
export default class trainingQuestions extends Component {
  constructor(props) {
    super(props);
    this.state = {
      emotion: {}
    };
    this.trainChat = this.trainChat.bind(this);
    this.emotionRecived = this.emotionRecived.bind(this);
  }
  emotionRecived(e) {
    Object.assign(this.state.emotion, e);
  }
  trainChat(e) {
    if (Object.keys(this.state.emotion).length > 0) {
      axios
        .post("/chat/train", {
          statement: this.props.statement,
          response: this.props.response,
          persona: "default",
          userid: "123",
          bad_response: e
        })
        .then(response => {})
        .catch(function(error) {
          console.log(error);
        });
      axios
        .post("/classify/add", {
          text: this.props.response,
          emotions: this.state.emotion
        })
        .then(response => {})
        .catch(function(error) {
          console.log(error);
        });

      this.props.return(true);
    } else {
      alert("Please move the relevant sliders");
    }
  }

  render() {
    const emotions = [
      "anger",
      "boredom",
      "empty",
      "enthusiasm",
      "fear",
      "fun",
      "happiness",
      "hate",
      "love",
      "neutral",
      "relief",
      "sadness",
      "surprise",
      "worry"
    ];

    const button = {
      borderRadius: 5,
      backgroundColor: "rgb(255,255,255,0.3)",
      color: "white",
      margin: ".5%",
      padding: ".5%",
      display: "inline-block",
      border: "0",

      outline: "0"
    };
    return (
      <div
        style={{
          border: "1px rgb(255,255,255,0.7) solid",
          margin: "1%",
          borderRadius: "25px"
        }}
      >
        <div>
          <br />
          <b>Correct Emotion</b>
          <br />
          Please move the <b>revelant</b> sliders to correct the emotion.
          <br />
          (Less --- More)
          <br />
          {emotions.map(emotion => (
            <EmotionSlider
              emotion={emotion}
              key={emotion}
              return={e => this.emotionRecived(e)}
            />
          ))}
          <br />
          Was "<b>{this.props.response}</b>" a good response to{" "}
          <b>"{this.props.statement}"</b> ?
          <br />
          <button style={button} onClick={() => this.trainChat(false)}>
            <b>YES</b>
          </button>
          <button style={button} onClick={() => this.trainChat(true)}>
            <b>NO</b>
          </button>
          <button style={button} onClick={() => this.trainChat("")}>
            <b>NOT SURE</b>
          </button>
        </div>
      </div>
    );
  }
}
