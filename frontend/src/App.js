import React from 'react';
import './App.css';

import {Route, Switch} from 'react-router-dom'
import { withRouter } from 'react-router-dom';

import 'antd/dist/antd.css';
import axios from 'axios'
import {Button} from 'antd'

import Home from './views/Home'
import Navbar from './views/Navbar'

import Battle from './views/Battle'

function App(props) {

  const handleClick = () => {
    const input = {
      number: '2'
    }
    axios.post(BASE_URL + '/game/', input).then(response =>{
      console.log(response)
    })
  }

  return (
    <div className="App">
      <header className="App-header">
        <Navbar/>
      </header>
      <Switch>
        <Route exact path = "/" component = {Home}/>
        <Route exact path = "/battle" component = {Battle}/>
      </Switch>
    </div>
  );
}

export default withRouter(App);
