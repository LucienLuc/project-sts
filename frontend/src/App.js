import React from 'react';
import './App.css';

import {Route, Switch} from 'react-router-dom'
import { withRouter } from 'react-router-dom';

function App(props) {
  return (
    <div className="App">
      <header className="App-header">
      </header>
      <p>
        Hello World!
      </p>
    </div>
  );
}

export default withRouter(App);
