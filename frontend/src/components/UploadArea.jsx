import { UploadCloud, ImagePlus } from "lucide-react";

const UploadArea = ({
  preview,
  loading,
  onFileChange,
  onPredict,
}) => {
  return (
    <div className="upload-section">

      {/* Upload Box */}
      <div className="upload-box">

        <input
          type="file"
          id="imageUpload"
          accept="image/*"
          hidden
          onChange={onFileChange}
        />

        <label htmlFor="imageUpload" className="upload-label">

          <UploadCloud
            size={60}
            className="upload-icon"
          />

          <h2>Drag & Drop Image</h2>

          <p>or Browse Files</p>

        </label>

      </div>

      {/* Preview Box */}
      <div className="preview-box">

        {preview ? (
          <>
            <img
              src={preview}
              alt="Preview"
              className="preview-image"
            />

            <div className="image-ready">
              ✓ Image Ready
            </div>
          </>
        ) : (
          <div className="preview-placeholder">

            <ImagePlus
              size={65}
              className="preview-icon"
            />

            <p>No Image Selected</p>

          </div>
        )}

      </div>

      {/* Button */}
      <button
        className="predict-button"
        onClick={onPredict}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Predict Digit"}
      </button>

    </div>
  );
};

export default UploadArea;