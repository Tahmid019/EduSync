import React from 'react'
import NavBar from './NavBar'
import "../css/login.css"
import Footer from './Footer';

function Login() {
    function myMenuFunction() {
        var i = document.getElementById("navMenu");

        if (i.classNameName === "nav-menu") {
            i.classNameName += " responsive";
        } else {
            i.classNameName = "nav-menu";
        }
    }

    var a = document.getElementById("loginBtn");
    var b = document.getElementById("registerBtn");
    var x = document.getElementById("login");
    var y = document.getElementById("register");

    function login() {
        x.style.left = "4px";
        y.style.right = "-520px";
        a.classNameName += " white-btn";
        b.classNameName = "btn";
        x.style.opacity = 1;
        y.style.opacity = 0;
    }

    function register() {
        x.style.left = "-510px";
        y.style.right = "5px";
        a.classNameName = "btn";
        b.classNameName += " white-btn";
        x.style.opacity = 0;
        y.style.opacity = 1;
    }
    return (
        <div id='loginbgimg'>
            <NavBar />
            <div className="wrapper">

                <div className="form-box">

                    <div className="login-container" id="login">
                        <div className="top">
                            <span>Don't have an account?
                                <a href="#" onclick={register}>Sign Up</a></span>
                            <header>Login</header>
                        </div>
                        <div className="input-box">
                            <input type="text" className="input-field" placeholder="Username or Email" />
                            <i className="bx bx-user"></i>
                        </div>
                        <div className="input-box">
                            <input type="password" className="input-field" placeholder="Password" />
                            <i className="bx bx-lock-alt"></i>
                        </div>
                        <div className="input-box">
                            <input type="submit" className="submit" value="Sign In" />
                        </div>
                        <div className="two-col">
                            <div className="one">
                                <input type="checkbox" id="login-check" />
                                <label for="login-check"> Remember Me</label>
                            </div>
                            <div className="two">
                                <label><a href="#">Forgot password?</a></label>
                            </div>
                        </div>
                    </div>

                    <div className="register-container" id="register">
                        <div className="top">
                            <span>Have an account? <a href="#" onclick={login}>Login</a></span>
                            <header>Sign Up</header>
                        </div>
                        <div className="two-forms">
                            <div className="input-box">
                                <input type="text" className="input-field" placeholder="Firstname" />
                                <i className="bx bx-user"></i>
                            </div>
                            <div className="input-box">
                                <input type="text" className="input-field" placeholder="Lastname" />
                                <i className="bx bx-user"></i>
                            </div>
                        </div>
                        <div className="input-box">
                            <input type="text" className="input-field" placeholder="Email" />
                            <i className="bx bx-envelope"></i>
                        </div>
                        <div className="input-box">
                            <input type="password" className="input-field" placeholder="Password" />
                            <i className="bx bx-lock-alt"></i>
                        </div>
                        <div className="input-box">
                            <input type="submit" className="submit" value="Register" />
                        </div>
                        <div className="two-col">
                            <div className="one">
                                <input type="checkbox" id="register-check" />
                                <label for="register-check"> Remember Me</label>
                            </div>
                            <div className="two">
                                <label><a href="#">Terms & conditions</a></label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login