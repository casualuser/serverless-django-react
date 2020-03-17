import React, { Component } from "react";
import { Button, Alert } from "antd";

class LandingPage extends Component {
  render() {
    const { handleLogin, loading, error } = this.props;

    return (
      <div
        style={{
          maxWidth: 600,
          height: "100%",
          margin: "0 auto",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column"
        }}
      >
        <Button loading={loading} size="large" onClick={handleLogin}>
          {loading
            ? "Logging in ..."
            : `Click here to ${error ? "try again" : "log in"}`}
        </Button>

        {!loading && error && (
          <Alert
            className="error"
            showIcon
            {...error}
            style={{ marginTop: 12 }}
          />
        )}
      </div>
    );
  }
}

export default LandingPage;
