import React, { useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
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
      const response = await axios.post('http://127.0.0.1:5000/image-predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log(response)

      if (response.data.prediction) {
        setPrediction(response.data.prediction);
      } else if (response.data.error) {
        setError(response.data.error);
      }
    } catch (error: any) {
      setError(error.response?.data?.error || 'An error occurred while making the prediction.');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>ASL Image Prediction</h1>

      <input type="file" accept="image/*" onChange={handleFileChange} />

      <button onClick={handleSubmit} style={{ margin: '10px', padding: '10px 20px' }}>
        Predict
      </button>

      {prediction && (
        <div style={{ marginTop: '20px', color: 'green' }}>
          <h3>Prediction: {prediction}</h3>
        </div>
      )}

      {error && (
        <div style={{ marginTop: '20px', color: 'red' }}>
          <h3>Error: {error}</h3>
        </div>
      )}
    </div>
  );
};

export default App;