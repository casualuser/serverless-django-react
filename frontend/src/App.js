import React, { Component, Suspense, lazy } from "react";
import { Switch, Route, withRouter } from "react-router-dom";
import { Button, Layout } from "antd";
import { authenticatedApplication } from "react-msal-jwt";
import axios from "axios";

import Forbidden from "./error/Forbidden";
import ServerError from "./error/ServerError";

import AppContext from "./AppContext";

import "./App.css";

import LandingPage from "./components/LandingPage";
const AdminDashboard = lazy(() => import("./components/AdminDashboard"));
const UserDashboard = lazy(() => import("./components/UserDashboard"));

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

    // If mounting the component on /error or /forbidden routes,
    // then redirect to the root route
    if (["/error", "/forbidden"].includes(props.location.pathname))
      props.history.replace("/");

    // Intercept requests to detect whether the access token is still valid
    axios.interceptors.request.use(
      async config => {
        const {
          access: hasAccessToken,
          refresh: hasRefreshToken
        } = props.isTokenExpired();

        // If the access token is invalid, and we are not interacting with auth endpoints,
        // then renew the access token
        if (
          !hasAccessToken &&
          !["auth/login/", "auth/refresh/", "auth/error/"].includes(config.url)
        ) {
          if (hasRefreshToken) {
            const accessToken = await props.refreshAccessToken();
            config.headers.common["Authorization"] = `Bearer ${accessToken}`;
          } else {
            props.throwTokenError();
          }
        }

        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );
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
              <h1 style={{ color: "#fff", margin: 0, fontSize: 32 }}>
                Example Application
              </h1>
            </div>

            <Button icon="poweroff" onClick={logout}>
              Log out
            </Button>
          </Layout.Header>

          <Layout.Content style={{ padding: 25 }}>
            <Layout style={{ padding: 25, background: "#fff" }}>
              <Suspense fallback={<div>Loading...</div>}>
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
              </Suspense>
            </Layout>
          </Layout.Content>
        </Layout>
      </AppContext.Provider>
    );
  }
}

export default authenticatedApplication({
  landingPage: <LandingPage />,
  msalConfig: {
    auth: {
      clientId: process.env.REACT_APP_AZURE_APP_ID,
      authority: process.env.REACT_APP_AZURE_AUTHORITY,
      redirectUri: process.env.REACT_APP_FRONTEND_URL
    }
  },
  onAuthSuccess: async (azureIdToken, azureAccessToken) => {
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
  onAuthError: error => {
    const { errorCode } = error;

    if (errorCode === "user_cancelled" || errorCode === "access_denied")
      return { type: "warning", message: "Login popup was closed." };
    else if (errorCode === "login_progress_error")
      return { type: "warning", message: "Login popup is already open." };
    else if (errorCode === "popup_window_error")
      return {
        type: "warning",
        message:
          "Error opening popup window. This can happen if you are using IE or if popups are blocked in the browser."
      };
    else if (error.message === "Network Error")
      return {
        type: "error",
        message: "Failed to communicate with the server."
      };

    const payload = {
      name: error.name,
      code: errorCode,
      message: error.message,
      stack: error.stack.toString().split("\n")
    };
    const headers = {
      "Content-Type": "application/json; charset=utf8",
      common: { Authorization: null }
    };
    axios.post("auth/error/", payload, { headers });

    return {
      type: "error",
      message: "An issue occurred while logging you in. Please try again."
    };
  },
  refreshAccess: async refresh => {
    const response = await axios.post("auth/refresh/", { refresh });

    const data = response.data;
    axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;

    return data.access;
  },
  tokenCheckFrequency: 2
})(withRouter(props => <App {...props} />));
