import React, { useState } from 'react';
import axios from 'axios';

const ImagePredict = () => {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('image', image);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/predict/', formData);
      setPrediction(response.data);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div>
      <h2>Upload Image for Location Prediction</h2>
      <input type="file" onChange={handleImageChange} />
      <button onClick={handleSubmit}>Predict Location</button>

      {prediction && (
        <div>
          <h3>Predicted Location: {prediction.location}</h3>
          <p>Latitude: {prediction.latitude}</p>
          <p>Longitude: {prediction.longitude}</p>
        </div>
      )}
    </div>
  );
};

export default ImagePredict;
