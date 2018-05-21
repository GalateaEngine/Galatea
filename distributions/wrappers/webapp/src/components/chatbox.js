import React, { Component } from "react";
import axios from "axios";
import { isBrowser } from "react-device-detect";
import TrainingQuestions from "./chatbox_components/trainingQuestions";
export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      enabled: true,
      placeholder: "Please type you reply",
      response: {
        text: "Hi...",
        emotion: "worry"
      }
    };

    this.emotionRecived = this.handleChange.bind(this);
    this.changeEmotion = this.changeEmotion.bind(this);
    this.chat = this.chat.bind(this);
  }

  chat(e) {
    if (e.length > 1) {
      this.setState({ previousText: e });
      axios
        .post("chat", {
          statement: e,
          persona: "default",
          userid: "123"
        })
        .then(response => {
          this.changeEmotion(response.data["response"]);

          Object.assign(this.state.response, {
            text: response.data["response"]
          });

          this.setState({ text: "" });
          this.setState({ enabled: true });
          if (isBrowser && response.data["response"] !== "...") {
            this.setState({ enabled: false });

            this.setState({
              placeholder: "Please respond to the questions above"
            });
          }
        })
        .catch(function(error) {
          console.log(error);
          alert("Sorry, the servers seem to be down");
        });
    }
  }

  changeEmotion(e) {
    axios
      .get("classify", {
        params: {
          text: e.toLowerCase()
        }
      })
      .then(response => {
        Object.assign(this.state.response, {
          emotion: response.data["classification"]
        });

        this.props.changePic(response.data["classification"]);
      });
  }

  handleChange(event) {
    this.setState({ text: event.target.value });
  }

  render() {
    return (
      <div>
        <div
          style={{
            width: "98%",
            backgroundColor: "rgb(65,62,74,0.7)",
            textAlign: "center",
            borderRadius: "25px 25px 0px 0px",
            padding: "1%",
            position: "absolute",
            bottom: "0"
          }}
        >
          <div
            style={{
              border: "1px rgb(255,255,255,0.7) solid",
              margin: "1%",
              borderRadius: "25px",
              display: "flex",
              padding: "2%",
              overflowWrap: "break-word"
            }}
          >
            {this.state.response.text}
          </div>
          {isBrowser ? (
            <div>
              {!this.state.enabled ? (
                <TrainingQuestions
                  statement={this.state.previousText}
                  response={this.state.response.text}
                  return={e => {
                    this.setState({
                      placeholder: "Please type you reply"
                    });
                    this.setState({ enabled: e });
                  }}
                />
              ) : (
                <div />
              )}
            </div>
          ) : (
            <b>{""}</b>
          )}
          <div
            style={{
              border: "1px rgb(255,255,255,0.7) solid",
              margin: "1%",
              borderRadius: "25px",
              display: "flex"
            }}
          >
            <br />
            <input
              placeholder={this.state.placeholder}
              type={"text"}
              disabled={!this.state.enabled}
              style={{
                borderRadius: 5,
                padding: "1%",

                borderColor: "white",
                background: "transparent",
                fontSize: "12px",
                flex: 2,
                outline: "none",
                border: "none",
                color: "white",
                margin: "1%",
                display: "inline-block",
                boxSizing: "border-box"
              }}
              value={this.state.text}
              onChange={this.handleChange.bind(this)}
              onKeyPress={event => {
                if (event.key === "Enter") {
                  this.chat(event.target.value);
                }
              }}
            />
          </div>
        </div>
      </div>
    );
  }
}
