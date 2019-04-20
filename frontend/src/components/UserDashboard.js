import React, { Component } from "react";
import { Spin, Icon } from "antd";

class UserDashboard extends Component {
  state = { loading: false };

  render() {
    const { loading } = this.state;

    if (loading)
      return (
        <div style={{ textAlign: "center" }}>
          <Spin size="large" indicator={<Icon type="loading" />} />
        </div>
      );

    return (
      <div>
        <h2>User dashboard</h2>
      </div>
    );
  }
}

export default UserDashboard;
