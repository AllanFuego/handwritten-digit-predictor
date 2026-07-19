import { LoaderCircle } from "lucide-react";

const Loader = () => {
  return (
    <div className="loader-container">

      <div className="loader-glow"></div>

      <LoaderCircle
        className="loader-icon"
        size={60}
        strokeWidth={2.5}
      />

      <h3>Analyzing Image...</h3>

      <p>
        Our AI model is identifying the handwritten digit.
      </p>

    </div>
  );
};

export default Loader;