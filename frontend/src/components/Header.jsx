import { BrainCircuit, Sparkles } from "lucide-react";

const Header = () => {
  return (
    <div className="header">

      <div className="logo-wrapper">

        <div className="logo-glow"></div>

        <div className="logo">

          <BrainCircuit size={42} strokeWidth={2.2} />

        </div>

      </div>

      <div className="header-content">

        <div className="title-row">

          <h1>Handwritten Digit Recognition</h1>

          <Sparkles
            size={22}
            className="sparkle-icon"
          />

        </div>

        <p>
          Upload a handwritten digit image and let our AI model
          recognize it instantly with high accuracy.
        </p>

      </div>

    </div>
  );
};

export default Header;