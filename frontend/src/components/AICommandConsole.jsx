import { useState } from "react";


function AICommandConsole() {
  const [output, setOutput] = useState(
    "COSMIC PARADOX AI CORE READY..."
  );

  const executeCommand = (command) => {
    switch (command) {
      case "scan":
        setOutput(`
> INITIATE CROP SCAN

Scanning PB-01...
Scanning PB-02...
Scanning PB-03...
Scanning PB-04...

STATUS: COMPLETE
`);
        break;

      case "advisory":
        setOutput(`
> GENERATE ADVISORY

PB-03:
Irrigation recommended
within 48 hours.

Risk Level: HIGH
Confidence: 92.4%
`);
        break;

      case "health":
        setOutput(`
> SYSTEM HEALTH

Satellite Link: ONLINE

AI Core: ACTIVE

Ground Relay: STABLE

Mission State: NOMINAL
`);
        break;

      case "predict":
        setOutput(`
> RISK PREDICTION

PB-04:

Projected moisture decline:
11%

Yield Impact Risk:
MODERATE

Action Required:
YES
`);
        break;

      default:
        setOutput("Awaiting Command...");
    }
  };

  const buttonStyle = {
    background:
      "linear-gradient(135deg,#001b34,#003b5c)",
    color: "#00ffff",
    border: "1px solid rgba(0,255,255,0.2)",
    borderRadius: "12px",
    padding: "12px",
    cursor: "pointer",
    fontWeight: "bold"
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
          color: "#00ffff",
          marginBottom: "10px"
        }}
      >
        TACTICAL AI COMMAND CONSOLE
      </h2>

      <div
        style={{
          color: "#7ddfff",
          fontSize: "13px",
          marginBottom: "20px",
          fontFamily: "monospace"
        }}
      >
        COSMIC PARADOX AI OPERATIONS CORE
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(200px,1fr))",
          gap: "12px",
          marginBottom: "20px"
        }}
      >
        <button
          style={buttonStyle}
          onClick={() => executeCommand("scan")}
        >
          INITIATE SCAN
        </button>

        <button
          style={buttonStyle}
          onClick={() => executeCommand("advisory")}
        >
          GENERATE ADVISORY
        </button>

        <button
          style={buttonStyle}
          onClick={() => executeCommand("health")}
        >
          SYSTEM HEALTH
        </button>

        <button
          style={buttonStyle}
          onClick={() => executeCommand("predict")}
        >
          PREDICT RISK
        </button>
      </div>

      <div
        style={{
          background: "#020814",
          border: "1px solid rgba(0,255,255,0.15)",
          borderRadius: "14px",
          padding: "20px",
          color: "#00ff88",
          fontFamily: "monospace",
          whiteSpace: "pre-line",
          minHeight: "220px"
        }}
      >
        {output}
      </div>
    </div>
  );
}

export default AICommandConsole;