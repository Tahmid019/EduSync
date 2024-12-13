import '../src/css/App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Abt from './pages/abt';
import Home from './pages/Home';
import Signup from './pages/Signup3';
import Login from './pages/Login1';
import Dashboard from './pages/Dashboard3';
import ErrorPage from './pages/ErrorPage';
// import express, { json, urlencoded } from 'express';
// import { createConnection } from 'mysql';
import React, {useEffect, useState} from 'react';
import Demo from './pages/Demo';
import Demoreview from './pages/Demoreview';


function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path='/' Component={Home}></Route>
          <Route path='/#signup' Component={Signup}></Route>
          <Route path='/signup' Component={Signup}></Route>
          <Route path='/#login' Component={Login}></Route>
          <Route path='/demo' Component={Demo}></Route>
          <Route path='/demo/review' Component={Demoreview}></Route>
          <Route path='/user' Component={Login}></Route>
          <Route path='/user/dashboard' Component={Dashboard}></Route>
          <Route path='/#ourteam' Component={Abt}></Route>
          <Route path='/ourteam' Component={Abt}></Route>
          <Route path='/dashboard' Component={Dashboard}></Route>
          <Route path='/#dashboard' Component={Dashboard}></Route>
          <Route path='/dashboard/translate' Component={Dashboard}></Route>
          <Route path='/*' Component={ErrorPage}></Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
