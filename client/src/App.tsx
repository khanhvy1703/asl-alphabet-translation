import React, { useState } from 'react';
import axios from 'axios';
import './App.css'

const App: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewURL, setPreviewURL] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setSelectedFile(file);
      setPreviewURL(URL.createObjectURL(file));
      setPrediction('');
      setError('');
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_ENDPOINT}/image-predict`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
        }
      );

      if (response.data.prediction) {
        setPrediction(response.data.prediction);
      } else {
        setError('Prediction failed.');
      }
    } catch (error: any) {
      setError(error.response?.data?.error || 'Prediction failed.');
    }
  };

  return (
    <div className="container">
      <h1>ASL Image Prediction</h1>

      <input type="file" accept="image/*" onChange={handleFileChange} className="input-file" />

      <button onClick={handleSubmit} className="predict-button">
        Predict
      </button>

      {previewURL && (
        <div className="preview-container">
          <img src={previewURL} alt="Selected" className="image-preview" />
        </div>
      )}

      {prediction && (
        <div className="result">
          <strong>Prediction:</strong> {prediction}
        </div>
      )}

      {error && (
        <div className="result error">
          <strong>Error:</strong> {error}
        </div>
      )}
    </div>
  );
};

export default App;
