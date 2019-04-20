import React from "react";
import { Button } from "antd";

import vault from "../img/403.svg";

class Forbidden extends React.Component {
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
        <img src={vault} alt="Forbidden" />

        <div style={{ marginLeft: 30 }}>
          <h1
            style={{
              fontWeight: 600,
              fontSize: 48,
              color: "#434e59",
              marginBottom: 0
            }}
          >
            Access denied
          </h1>

          <div
            style={{ fontSize: 20, color: "rgba(0,0,0,.45)", marginBottom: 30 }}
          >
            Sorry, you don't have access to this page.
          </div>

          <Button type="primary" size="large" onClick={() => history.push("/")}>
            Back to home
          </Button>
        </div>
      </div>
    );
  }
}

export default Forbidden;
