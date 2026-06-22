import { useState } from "react";

function DigitalTwin({ selectedZone }) {
  const [hoveredZone, setHoveredZone] =
    useState(null);

  const zones = [
    {
      id: "PB-01",
      status: "HEALTHY",
      color: "#00ff88",
      score: "94%"
    },
    {
      id: "PB-02",
      status: "WATCH",
      color: "#ffd700",
      score: "81%"
    },
    {
      id: "PB-03",
      status: "WARNING",
      color: "#ff9900",
      score: "68%"
    },
    {
      id: "PB-04",
      status: "CRITICAL",
      color: "#ff4444",
      score: "42%"
    }
  ];

  return (
    <div
      style={{
        background: "rgba(10,15,35,0.7)",
        border: "1px solid rgba(0,255,255,0.2)",
        borderRadius: "24px",
        padding: "25px",
        marginTop: "25px",
        backdropFilter: "blur(12px)"
      }}
    >
      <h2
        style={{
          color: "#00ffff",
          marginBottom: "8px"
        }}
      >
        DIGITAL TWIN
      </h2>

      <div
        style={{
          color: "#7ddfff",
          fontSize: "13px",
          marginBottom: "20px",
          fontFamily: "monospace"
        }}
      >
        AGRICULTURAL SYSTEM MODEL
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "15px"
        }}
      >
        {zones.map((zone) => (
          <div
            key={zone.id}
            onMouseEnter={() =>
              setHoveredZone(zone.id)
            }
            onMouseLeave={() =>
              setHoveredZone(null)
            }
            style={{
              background: "rgba(0,15,35,0.55)",

              border:
                zone.id === selectedZone
                  ? `2px solid ${zone.color}`
                  : `1px solid rgba(0,255,255,0.1)`,

              borderRadius: "18px",
              padding: "18px",

              cursor: "pointer",

              transition: "all 0.3s ease",

              transform:
                hoveredZone === zone.id
                  ? "translateY(-6px)"
                  : "translateY(0px)",

              boxShadow:
                zone.id === selectedZone
                  ? `0 0 30px ${zone.color}`
                  : hoveredZone === zone.id
                  ? `0 0 20px ${zone.color}`
                  : "none"
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: "15px"
              }}
            >
              <div
                style={{
                  color: "#c8f8ff",
                  fontWeight: "bold"
                }}
              >
                {zone.id}
              </div>

              <div
                style={{
                  color: zone.color,
                  fontWeight: "bold"
                }}
              >
                {zone.score}
              </div>
            </div>

            <div
              style={{
                height: "10px",
                background: "#0b1324",
                borderRadius: "20px",
                overflow: "hidden",
                marginBottom: "15px"
              }}
            >
              <div
                style={{
                  width: zone.score,
                  height: "100%",
                  background: zone.color
                }}
              />
            </div>

            <div
              style={{
                color: zone.color,
                fontSize: "13px",
                fontWeight: "bold"
              }}
            >
              {zone.status}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DigitalTwin;