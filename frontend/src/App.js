import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";
import { Button, Layout, Alert } from "antd";
import { authenticatedApplication } from "react-msal-jwt";
import { LandingPage } from "login-landing-page";
import axios from "axios";

import AdminDashboard from "./components/AdminDashboard";
import UserDashboard from "./components/UserDashboard";
import Forbidden from "./error/Forbidden";
import ServerError from "./error/ServerError";

import AppContext from "./AppContext";

axios.defaults.baseURL = process.env.REACT_APP_BACKEND_URL;

axios.defaults.headers.common[
  "Authorization"
] = `Bearer ${sessionStorage.getItem("access")}`;

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isAdmin: props.isAdmin || sessionStorage.getItem("isAdmin") === "true"
    };
  }

  render() {
    const { getAzureToken, logout } = this.props;
    const { isAdmin } = this.state;

    return (
      <AppContext.Provider value={{ getAzureToken, isAdmin }}>
        <Layout style={{ height: "100%" }}>
          <Layout.Header style={{ display: "flex", alignItems: "center" }}>
            <div
              style={{
                flex: 1,
                display: "flex",
                alignItems: "center",
                height: "100%"
              }}
            >
              <img
                src="https://cdn.teaching.unsw.edu.au/unswbranding/unsw_neg.png"
                alt="UNSW logo"
                style={{
                  maxHeight: "100%",
                  width: "auto",
                  padding: "10px 0",
                  marginRight: 25
                }}
              />

              <h1 style={{ color: "#fff", margin: 0, fontSize: 32 }}>
                Boilerplate
              </h1>
            </div>

            <Button icon="poweroff" onClick={logout}>
              Log out
            </Button>
          </Layout.Header>

          <Layout.Content style={{ padding: 25 }}>
            <Layout style={{ padding: 25, background: "#fff" }}>
              <Switch>
                <Route
                  exact
                  path="/"
                  render={props =>
                    isAdmin ? (
                      <AdminDashboard {...props} />
                    ) : (
                      <UserDashboard {...props} />
                    )
                  }
                />

                <Route exact path="/forbidden" component={Forbidden} />
                <Route exact path="/error" component={ServerError} />
              </Switch>
            </Layout>
          </Layout.Content>
        </Layout>
      </AppContext.Provider>
    );
  }
}

export default authenticatedApplication({
  landingPage: (
    <LandingPage
      title="Boilerplate"
      background="https://cdn.teaching.unsw.edu.au/161006_UNSW_016.jpg"
      logo={
        <a href="https://www.unsw.edu.au/">
          <img
            src="https://cdn.teaching.unsw.edu.au/unswbranding/unsw_neg.png"
            alt="UNSW Logo"
          />
        </a>
      }
      welcomeMessage={
        <Alert
          showIcon
          type="warning"
          message={
            <>
              Please log in using <strong>{`<Your zID>`}@ad.unsw.edu.au</strong>
            </>
          }
        />
      }
      errorMessage={
        <Alert
          showIcon
          type="error"
          message={
            <>
              An issue occured while logging you in. Please click the button
              below to sign out from any other sessions and try again, ensuring
              that you use <strong>{`<Your zID>`}@ad.unsw.edu.au</strong> when
              you next log in. If the problem persists, please clear your
              browser cache and try again.
            </>
          }
        />
      }
      footerItems={[
        <a href="mailto:contact.pvce@unsw.edu.au">Contact us</a>,
        <a href="https://www.unsw.edu.au/privacy">Privacy Policy</a>,
        <a href="https://www.unsw.edu.au/copyright-disclaimer">
          Copyright &amp; Disclaimer
        </a>
      ]}
    />
  ),
  msalConfig: {
    clientId: process.env.REACT_APP_AZURE_APP_ID,
    redirectUri: process.env.REACT_APP_FRONTEND_URL,
    authority: process.env.REACT_APP_AZURE_AUTHORITY
  },
  authCallback: async (azureIdToken, azureAccessToken) => {
    const headers = {
      "Content-Type": "application/json; charset=utf8",
      Authorization: "Token " + azureIdToken
    };
    const response = await axios.post(
      "auth/login/",
      { accessToken: azureAccessToken },
      { headers }
    );

    const data = response.data;
    axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;
    sessionStorage.setItem("isAdmin", data.is_admin);

    return {
      accessToken: data.access,
      refreshToken: data.refresh,
      extras: {
        isAdmin: data.is_admin
      }
    };
  },
  refreshAccess: async refresh => {
    const response = await axios.post("auth/refresh/", { refresh });

    const data = response.data;
    axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;

    return data.access;
  }
})(App);
