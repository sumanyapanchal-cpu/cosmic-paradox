import { useEffect, useState } from "react";

function LiveTelemetry() {
  const [ndvi, setNdvi] = useState(68);
  const [moisture, setMoisture] = useState(72);
  const [satellite, setSatellite] = useState(94);

  useEffect(() => {
    const interval = setInterval(() => {
      setNdvi(
        (prev) =>
          Math.max(
            50,
            Math.min(
              90,
              prev + Math.floor(Math.random() * 5) - 2
            )
          )
      );

      setMoisture(
        (prev) =>
          Math.max(
            40,
            Math.min(
              100,
              prev + Math.floor(Math.random() * 5) - 2
            )
          )
      );

      setSatellite(
        (prev) =>
          Math.max(
            85,
            Math.min(
              100,
              prev + Math.floor(Math.random() * 3) - 1
            )
          )
      );
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const cardStyle = {
    background: "rgba(0,15,35,0.55)",
    border: "1px solid rgba(0,255,255,0.12)",
    borderRadius: "16px",
    padding: "18px",
    textAlign: "center"
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
          marginBottom: "20px"
        }}
      >
        LIVE SATELLITE TELEMETRY
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "15px"
        }}
      >
        <div style={cardStyle}>
          <div style={{ color: "#7ddfff" }}>
            NDVI INDEX
          </div>

          <div
            style={{
              color: "#00ff88",
              fontSize: "32px",
              fontWeight: "bold"
            }}
          >
            {ndvi}
          </div>
        </div>

        <div style={cardStyle}>
          <div style={{ color: "#7ddfff" }}>
            MOISTURE
          </div>

          <div
            style={{
              color: "#00ffff",
              fontSize: "32px",
              fontWeight: "bold"
            }}
          >
            {moisture}%
          </div>
        </div>

        <div style={cardStyle}>
          <div style={{ color: "#7ddfff" }}>
            SATELLITE LINK
          </div>

          <div
            style={{
              color: "#ffd700",
              fontSize: "32px",
              fontWeight: "bold"
            }}
          >
            {satellite}%
          </div>
        </div>
      </div>
    </div>
  );
}

export default LiveTelemetry;