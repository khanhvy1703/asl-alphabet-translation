import React, { useState } from "react";
import { predictASL } from "./services/image";

function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [error, setError] = useState("");

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
    setPrediction("");
    setError("");
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!image) {
      setError("Please select an image first.");
      return;
    }

    try {
      const result = await predictASL(image);
      setPrediction(result.prediction);
    } catch (err) {
      setError("An error occurred while processing the image.");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>ASL Predictor</h1>
      <form onSubmit={handleFormSubmit}>
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <button type="submit" style={{ marginLeft: "10px" }}>
          Predict
        </button>
      </form>
      {prediction && (
        <div style={{ marginTop: "20px" }}>
          <h2>Prediction: {prediction}</h2>
        </div>
      )}
      {error && (
        <div style={{ color: "red", marginTop: "20px" }}>
          <h3>{error}</h3>
        </div>
      )}
    </div>
  );
}

export default App;
