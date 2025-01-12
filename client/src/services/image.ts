import axios from 'axios';

// Get the base URL from the environment variable
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const predictASL = async (imageFile) => {
  const formData = new FormData();
  formData.append("image", imageFile);

  try {
    const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error predicting ASL:", error);
    throw error.response ? error.response.data : error.message;
  }
};
