import { useState } from "react";

function AICopilot() {
  const [response, setResponse] = useState(
    "Awaiting Command..."
  );

  const runPrompt = (prompt) => {
    if (prompt === "health") {
      setResponse(`
ZONE PB-03

STATUS: WARNING

NDVI decline detected.

Recommended irrigation:
WITHIN 48 HOURS

Confidence: 92.4%
`);
    }

    else if (prompt === "report") {
      setResponse(`
MISSION REPORT

4 zones analyzed

1 critical

1 warning

2 stable

Satellite coverage nominal.
`);
    }

    else {
      setResponse(`
IRRIGATION ADVISORY

Increase moisture levels.

Monitor next satellite pass.

No severe anomaly detected.
`);
    }
  };

  return (
    <div
      style={{
        background: "rgba(10,15,35,0.7)",
        border: "1px solid rgba(0,255,255,0.2)",
        borderRadius: "24px",
        padding: "25px",
        marginTop: "25px"
      }}
    >
      <h2
        style={{
          color: "#00ffff"
        }}
      >
        AI COPILOT
      </h2>

      <div
        style={{
          marginTop: "20px",
          display: "flex",
          gap: "10px",
          flexWrap: "wrap"
        }}
      >
        <button
          onClick={() => runPrompt("health")}
        >
          Zone Health
        </button>

        <button
          onClick={() => runPrompt("report")}
        >
          Mission Report
        </button>

        <button
          onClick={() => runPrompt("advisory")}
        >
          Irrigation Plan
        </button>
      </div>

      <div
        style={{
          marginTop: "20px",
          background: "rgba(0,15,35,0.55)",
          border: "1px solid rgba(0,255,255,0.12)",
          borderRadius: "14px",
          padding: "18px",
          color: "#c8f8ff",
          whiteSpace: "pre-line",
          fontFamily: "monospace"
        }}
      >
        {response}
      </div>
    </div>
  );
}

export default AICopilot;