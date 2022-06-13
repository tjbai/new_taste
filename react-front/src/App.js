import React, { useState, useEffect } from 'react';
import './App.css';

import { WebcamSource } from './Components/WebcamSource';

function App() {
  return (
    <div className="App">
      <WebcamSource/> 
    </div>
  );
}

export default App;
