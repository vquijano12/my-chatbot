import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const generateResponse = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/generate`, data);
    return response.data;
  } catch (error) {
    console.error("Error generating response:", error);
    throw error;
  }
};
