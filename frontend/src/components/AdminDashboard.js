import React, { Component } from "react";
import { Spin, Icon } from "antd";
import axios from "axios";

import AppContext from "../AppContext";

class AdminDashboard extends Component {
  static contextType = AppContext;

  state = { loading: true };

  componentWillMount() {
    const { history } = this.props;
    const { getAzureToken } = this.context;

    // Example API call that would enable the backend to perform a 
    // MS Graph call using the Azure token generated
    getAzureToken().then(accessToken =>
      axios
        .post("admin/", { accessToken })
        .then(res => {
          const { data } = res.data;
          this.setState({
            loading: false,
            data
          });
        })
        .catch(error => {
          if (error.response.status === 403) {
            history.replace("/forbidden");
            return;
          }

          history.replace("/error");
        })
    );
  }

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
        <h2>Administrative dashboard</h2>
        Test
      </div>
    );
  }
}

export default AdminDashboard;
