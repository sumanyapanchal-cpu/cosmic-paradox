import { useState } from "react";
import SatelliteOrbit from "./SatelliteOrbit";
import NDVIGraph from "./NDVIGraph";

function CommandCenter({
  selectedZone,
  setSelectedZone
}) {
  const zones = [
    {
      id: "PB-01",
      crop: "Rice",
      priority: "LOW",
      action: "Monitor moisture conditions"
    },
    {
      id: "PB-02",
      crop: "Cotton",
      priority: "MEDIUM",
      action: "Schedule irrigation in 72 hours"
    },
    {
      id: "PB-03",
      crop: "Wheat",
      priority: "HIGH",
      action: "Initiate irrigation within 48 hours"
    },
    {
      id: "PB-04",
      crop: "Maize",
      priority: "CRITICAL",
      action: "Immediate intervention required"
    }
  ];

  

  const [brief, setBrief] = useState(
    "Awaiting Mission Generation..."
  );

  const panelStyle = {
    background: "rgba(10,15,35,0.7)",
    border: "1px solid rgba(0,255,255,0.2)",
    borderRadius: "24px",
    padding: "25px",
    backdropFilter: "blur(12px)",
    minHeight: "260px"
  };

  const generateBrief = () => {
  if (selectedZone === "PB-01") {
    setBrief(`
ZONE: PB-01

CROP: Rice

STATUS: HEALTHY

AI ADVISORY:
Maintain current irrigation schedule.

RISK LEVEL:
LOW

CONFIDENCE:
94.2%
`);
  }

  else if (selectedZone ==="PB-02") {
    setBrief(`
ZONE: PB-02

CROP: Cotton

STATUS: WATCH

AI ADVISORY:
Monitor moisture decline over next 72 hours.

RISK LEVEL:
MEDIUM

CONFIDENCE:
91.7%
`);
  }

  else if (selectedZone=== "PB-03") {
    setBrief(`
ZONE: PB-03

CROP: Wheat

STATUS: WARNING

AI ADVISORY:
Initiate irrigation within 48 hours.

RISK LEVEL:
HIGH

CONFIDENCE:
92.4%
`);
  }

  else {
    setBrief(`
ZONE: PB-04

CROP: Maize

STATUS: CRITICAL

AI ADVISORY:
Immediate irrigation required.

Potential yield reduction detected.

RISK LEVEL:
CRITICAL

CONFIDENCE:
96.1%
`);
  }
};
    return (
  <>
      {/* ZONE SELECTOR */}
      <div
        style={{
          display: "flex",
          gap: "12px",
          justifyContent: "center",
          marginBottom: "25px",
          flexWrap: "wrap"
        }}
      >
        {zones.map((zone) => (
          <button
            key={zone.id}
            onClick={() => setSelectedZone(zone.id)}
            style={{
              padding: "10px 18px",
              background:
                selectedZone === zone.id
                  ? "#00ffff"
                  : "#112244",
              color:
                selectedZone=== zone.id
                  ? "#000"
                  : "#fff",
              border: "none",
              borderRadius: "10px",
              cursor: "pointer",
              fontWeight: "bold"
            }}
          >
            {zone.id}
          </button>
        ))}
      </div>

      {/* GENERATE BUTTON */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginBottom: "30px"
        }}
      >
        <button
          onClick={generateBrief}
          style={{
            padding: "16px 32px",
            background:
              "linear-gradient(135deg,#00ffff,#0099ff)",
            color: "#001018",
            border: "none",
            borderRadius: "14px",
            fontWeight: "bold",
            fontSize: "16px",
            cursor: "pointer",
            boxShadow:
              "0 0 25px rgba(0,255,255,0.5)"
          }}
        >
          GENERATE AI ADVISORY
        </button>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "25px",
          marginTop: "20px"
        }}
      >
        {/* MISSION MAP */}
<div style={panelStyle}>
  <h2 style={{ color: "#00ffff" }}>
    MISSION MAP
  </h2>

  <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      marginTop: "20px"
    }}
  >
    <SatelliteOrbit />
  </div>
</div>

        {/* LIVE FEED */}
        <div style={panelStyle}>
          <h2 style={{ color: "#00ffff" }}>
            LIVE FEED
          </h2>

          <div
            style={{
              marginTop: "15px",
              fontFamily: "monospace",
              fontSize: "14px",
              lineHeight: "28px",
              color: "#9cf6ff",
              background: "rgba(0,0,0,0.25)",
              padding: "15px",
              borderRadius: "10px",
              border:
                "1px solid rgba(0,255,255,0.15)"
            }}
          >
            <div>[18:41] Sentinel-2 Updated</div>
            <div>[18:42] Moisture Analysis Complete</div>
            <div>[18:43] Punjab Node Active</div>
            <div>[18:44] Advisory Generated</div>
            <div>[18:45] Crop Stress Scan Running</div>
          </div>
        </div>

        {/* ANALYTICS */}
        <div style={panelStyle}>
          <h2 style={{ color: "#00ffff" }}>
            ANALYTICS
          </h2>

          <div
            style={{
              marginTop: "20px",
              fontFamily: "monospace",
              lineHeight: "35px"
            }}
          >
            <NDVIGraph />
          </div>
        </div>

        {/* MISSION BRIEF */}
        <div style={panelStyle}>
          <h2 style={{ color: "#00ffff" }}>
            MISSION BRIEF
          </h2>

          <div
            style={{
              background: "rgba(0,0,0,0.35)",
              border:
                "1px solid rgba(0,255,255,0.15)",
              borderRadius: "12px",
              padding: "20px",
              marginTop: "20px",
              fontFamily: "monospace",
              color: "#9cf6ff",
              lineHeight: "28px",
              whiteSpace: "pre-line"
            }}
          >
            {brief}
          </div>
        </div>
      </div>
    </>
  );
}

export default CommandCenter;