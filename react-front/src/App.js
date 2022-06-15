import React, { useState, useEffect } from 'react';
import './App.css';

import Body from './Components/Body';

function App() {
  return (
    <div className="App">
      <header>Please center your face in the webcam</header>
      <Body /> 
    </div>
  );
}

export default App;
