import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import "../css/login.css";

function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    u_fname: '',
    u_lname: '',
    u_mail: '',
    u_pass: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior
    if (!formData.u_mail || !formData.u_pass) {
      console.error('Email and password are required');
      return;
    }

    console.log('Sending data:', formData); // Log the form data to console

    try {
      const response = await fetch('/user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Server response:', result); // Log the server response to console
        navigate('/user');
      } else {
        console.error('Error sending data:', await response.text());
      }
    } catch (error) {
      console.error('Error:', error);
    }
    navigate('/user')
  };

  return (
    <div style={{ backgroundImage: "url(../images/loginbg.jpg)", overflowY: "hidden", width: "100vw" }}>
      <NavBar />
      <div className="wrapper" style={{ backgroundColor: "hsl(190, 64%, 22%)" }}>
        <div className="form-box">
          <form className="register-container" id="register" onSubmit={handleSubmit}>
            <div className="top">
              <span>Have an account? <Link to="/user">Login</Link></span>
              <header>Sign Up</header>
            </div>
            <div className="two-forms">
              <div className="input-box">
                <input id='usrfname' type="text" className="input-field" name="u_fname" value={formData.u_fname} onChange={handleChange} placeholder="First Name" />
                <i className="bx bx-user"></i>
              </div>
              <div className="input-box">
                <input id='usrlname' type="text" className="input-field" name="u_lname" value={formData.u_lname} onChange={handleChange} placeholder="Last Name" />
                <i className="bx bx-user"></i>
              </div>
            </div>
            <div className="input-box">
              <input id='usrmail' type="text" className="input-field" name="u_mail" value={formData.u_mail} onChange={handleChange} placeholder="Email" />
              <i className="bx bx-envelope"></i>
            </div>
            <div className="input-box">
              <input id='usrpasscode' type="password" className="input-field" name="u_pass" value={formData.u_pass} onChange={handleChange} placeholder="Password" />
              <i className="bx bx-lock-alt"></i>
            </div>
            <div className="input-box">
              <input type="submit" className="submit" value="Register" />
            </div>
            <div className="two-col">
              <div className="one">
                <input type="checkbox" id="register-check" />
                <label htmlFor="register-check"> Remember Me</label>
              </div>
              <div className="two">
                <label><a href="#">Terms & conditions</a></label>
              </div>
            </div>
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Signup;
