import React from "react";

const Background = () => {
  return (
    <>
      <div className="background">
        <div className="gradient gradient1"></div>
        <div className="gradient gradient2"></div>
        <div className="gradient gradient3"></div>

        <div className="blob blob1"></div>
        <div className="blob blob2"></div>
        <div className="blob blob3"></div>
        <div className="blob blob4"></div>

        <div className="stars">
          {Array.from({ length: 30 }).map((_, index) => (
            <span
              key={index}
              className="star"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 8}s`,
              }}
            ></span>
          ))}
        </div>
      </div>
    </>
  );
};

export default Background;