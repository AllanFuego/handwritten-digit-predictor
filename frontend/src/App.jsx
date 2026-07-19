import { useState } from "react";
import axios from "axios";

import "./App.css";

import Background from "./components/Background";
import Header from "./components/Header";
import UploadArea from "./components/UploadArea";
import Loader from "./components/Loader";
import ResultCard from "./components/ResultCard";

// Vite uses import.meta.env
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
console.log("🔍 API_URL:", API_URL);
console.log("🔍 All env vars:", import.meta.env);

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const handlePredict = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);

    try {
      console.log("📤 Sending to:", `${API_URL}/predict`);
      
      const response = await axios.post(
        `${API_URL}/predict`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          timeout: 30000, // 30 seconds timeout
        }
      );

      console.log("✅ Response:", response.data);
      setResult(response.data);
    } catch (error) {
      console.error("❌ Error:", error);
      
      if (error.response) {
        alert(`Error ${error.response.status}: ${error.response.data?.detail || "Prediction failed"}`);
      } else if (error.request) {
        alert("Cannot connect to backend. Please try again later.");
      } else {
        alert("Error: " + error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Background />

      <div className="app">
        <Header />

        <UploadArea
          preview={preview}
          loading={loading}
          onFileChange={handleFileChange}
          onPredict={handlePredict}
        />

        {loading && <Loader />}

        {!loading && result && (
          <ResultCard
            prediction={result.prediction}
            confidence={result.confidence}
            model={result.model}
            accuracy={result.accuracy}
            precision={result.precision}
            recall={result.recall}
            f1Score={result.f1_score}
          />
        )}
      </div>
    </>
  );
}

export default App;