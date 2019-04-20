import React from "react";
import { Button } from "antd";

import error from "../img/500.svg";

class ServerError extends React.Component {
  render() {
    const { history } = this.props;

    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flex: "auto",
          margin: "40px 0"
        }}
      >
        <img src={error} alt="Server Error" />

        <div style={{ marginLeft: 30 }}>
          <h1
            style={{
              fontWeight: 600,
              fontSize: 48,
              color: "#434e59",
              marginBottom: 0
            }}
          >
            Server error
          </h1>

          <div
            style={{ fontSize: 20, color: "rgba(0,0,0,.45)", marginBottom: 30 }}
          >
            Sorry, the server is reporting an error.
          </div>

          <Button type="primary" size="large" onClick={() => history.push("/")}>
            Back to home
          </Button>
        </div>
      </div>
    );
  }
}

export default ServerError;
