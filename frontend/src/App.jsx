import { useState } from "react";
import axios from "axios";

import "./App.css";

import Background from "./components/Background";
import Header from "./components/Header";
import UploadArea from "./components/UploadArea";
import Loader from "./components/Loader";
import ResultCard from "./components/ResultCard";

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
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert(
        error.response?.data?.detail ||
          "Prediction failed. Please try again."
      );
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