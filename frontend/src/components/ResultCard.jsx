import {
  CheckCircle2,
  Cpu,
  BarChart3,
  Award,
  Target,
} from "lucide-react";

function ResultCard({
  prediction,
  confidence,
  model,
  accuracy,
  precision,
  recall,
  f1Score,
}) {
  return (
    <div className="result-card">

      <div className="result-header">
        <CheckCircle2 size={28} />
        <h2>Prediction Result</h2>
      </div>

      <div className="prediction-number">
        {prediction}
      </div>

      <div className="confidence-section">
        <div className="confidence-header">
          <span>Confidence</span>
          <span>{confidence ?? "--"}%</span>
        </div>

        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{
              width: `${confidence ?? 0}%`,
            }}
          ></div>
        </div>
      </div>

      <div className="metrics">

        <div className="metric">
          <Cpu size={20} />
          <div>
            <p>Model</p>
            <h4>{model}</h4>
          </div>
        </div>

        <div className="metric">
          <BarChart3 size={20} />
          <div>
            <p>Accuracy</p>
            <h4>{accuracy}%</h4>
          </div>
        </div>

        <div className="metric">
          <Target size={20} />
          <div>
            <p>Precision</p>
            <h4>{precision}%</h4>
          </div>
        </div>

        <div className="metric">
          <Target size={20} />
          <div>
            <p>Recall</p>
            <h4>{recall}%</h4>
          </div>
        </div>

        <div className="metric">
          <Award size={20} />
          <div>
            <p>F1 Score</p>
            <h4>{f1Score}%</h4>
          </div>
        </div>

      </div>
    </div>
  );
}

export default ResultCard;