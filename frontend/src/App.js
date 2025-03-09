import React from 'react';
import './App.css';
import LocationData from './LocationData';
import ImagePredict from './ImagePredict';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <ImagePredict />
        <LocationData />
      </header>
    </div>
  );
}

export default App;
