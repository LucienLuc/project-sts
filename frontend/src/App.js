import React from 'react';
import './App.css';

import {Route, Switch} from 'react-router-dom'
import { withRouter } from 'react-router-dom';

import axios from 'axios'
import {Button} from 'antd'

const BASE_URL = 'https://project-sts-backend.herokuapp.com'
//const BASE_URL = 'http://127.0.0.1:8000'

function App(props) {

  const handleClick = () => {
    const input = {
      number: '2'
    }
    axios.post(BASE_URL + '/test/', input).then(response =>{
      console.log(response)
    })
  }

  return (
    <div className="App">
      <header className="App-header">
      </header>
      <p>
        Hello World!
      </p>
      <Button onClick = {handleClick}>
        Test
      </Button>
    </div>
  );
}

export default withRouter(App);
