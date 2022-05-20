import React, { FormEvent } from "react";
import autoBind from "auto-bind";
import urlJoin from "url-join";

import CircularIndeterminate from "../components/circular_indeterminate_progress";

import "./LoginScreen.css";

enum LoginState {
    CHECKING_LOGIN_STATUS,
    WAITING_USER_INPUT,
    LOGGING_IN,
    FAILED_LOGIN,
    LOGGED_IN,
};

interface LoginArguments {
    onLoginSucceeded: Function;
}

interface _LoginState {
    loginState: LoginState;
    currentUsername?: string;
}


export default class LoginScreen extends React.Component<LoginArguments, _LoginState> {
    private readonly usernameRef = React.createRef<HTMLInputElement>();

    constructor(props: LoginArguments) {
        super(props);
        autoBind(this);

        this.state = {
            loginState: LoginState.CHECKING_LOGIN_STATUS,
        };
    }

    componentDidMount() {
        this.checkLoginStatus();
    }

    componentDidUpdate() {
        if (this.state.currentUsername) {
            this.usernameRef.current?.setAttribute("value", this.state.currentUsername)
        }
    }

    loginTitle(): any {
        return <h1 className={"login-body-title"}>Login</h1>;
    }

    mainLoginForm(): any {
        return [
            <input placeholder={"Username"} name={"username"} className={"login-text-field login-field"} autoComplete={"username"} key={1} ref={this.usernameRef}/>,
            <input type={"password"} placeholder={"Password"} name={"password"} className={"login-text-field login-field"} autoComplete={"current-password"} key={2}/>,
            <input type={"submit"} className={"login-submit-button login-field"} value={"Login"} key={3}/>,
        ];
    }

    render(): any {
        switch (this.state.loginState) {
            case LoginState.WAITING_USER_INPUT:
                return (<div className={"login-screen"} >
                    <form className={"login-body-container"} onSubmit={this.onLoginClicked}>
                        {this.loginTitle()}
                        {this.mainLoginForm()}
                        </form>
                </div>);
            case LoginState.LOGGING_IN:
                return (<div className={"login-screen"}>
                    <form className={"login-body-container"} onSubmit={this.onLoginClicked}>
                        {this.loginTitle()}
                        <div className={"login-screen-wait-text"}>
                            Logging in, please wait...
                        </div>
                        <LoginProgressBar />
                    </form>
                </div>)
            case LoginState.FAILED_LOGIN:
                return (<div className={"login-screen has-errors"} >
                    <form className={"login-body-container"} onSubmit={this.onLoginClicked}>
                        {this.loginTitle()}
                        <div className={"login-screen-error-text"}>
                            Invalid username or password.
                        </div>
                        {this.mainLoginForm()}
                    </form>
                </div>);
            case LoginState.LOGGED_IN:
                return (<div className={"login-screen"}>
                    <form className={"login-body-container"} onSubmit={this.onLoginClicked}>
                        {this.loginTitle()}
                        <p className={"login-screen-success-text"}>
                            Logged in successfully, please wait...
                        </p>
                    </form>
                </div>)
        }
    }

    async checkLoginStatus() {
        console.debug("checking login status");

        let isLoggedIn = false;

        if (process.env.NODE_ENV !== "production") {
            await new Promise((resolve) => {
                setTimeout(resolve, 1000);
            });
            isLoggedIn = false;
        } else {
            let statusUrl = "/login/status/";

            if (process.env.PUBLIC_URL) {
                statusUrl = urlJoin(process.env.PUBLIC_URL, statusUrl);
            }

            const response = await fetch(statusUrl);
            const data = await response.text();

            isLoggedIn = response.ok && data === "true";
        }

        if (!isLoggedIn) {
            this.setState({loginState: LoginState.WAITING_USER_INPUT});
        } else {
            this.setState({ loginState: LoginState.LOGGED_IN });
            this.props.onLoginSucceeded();
        }
    }

    async onLoginClicked(event: FormEvent<HTMLFormElement>) {
        console.debug("on login clicked");
        event.preventDefault();

        let formData = new FormData(event.currentTarget);

        this.setState({ loginState: LoginState.LOGGING_IN, currentUsername: formData.get("username")?.toString()});
        let successful = false;

        if (process.env.NODE_ENV !== "production") {
            await new Promise((resolve) => {
                setTimeout(resolve, 1000);
            });
            successful = true;
        } else {
            console.debug(process.env.PUBLIC_URL)
            let loginUrl = urlJoin("login", "post");

            if (process.env.PUBLIC_URL) {
                loginUrl = urlJoin(process.env.PUBLIC_URL, loginUrl);
            }

            const response = await fetch(loginUrl, { body: formData, method: "POST" });
            successful = response.ok;
        }

        if (!successful) {
            console.debug("login failed");
            this.setState({ loginState: LoginState.FAILED_LOGIN });
        } else {
            this.setState({ loginState: LoginState.LOGGED_IN });
            this.props.onLoginSucceeded();
        }
    }
}

function LoginProgressBar(props: any): any {
    return (<div className={"login-progress-bar-container"}>
        <CircularIndeterminate />
    </div>);
}
