function ThreatHeatmap() {
  const sectors = [
    { id: "A1", risk: "LOW", color: "#00ff88" },
    { id: "A2", risk: "WATCH", color: "#ffd700" },
    { id: "A3", risk: "LOW", color: "#00ff88" },

    { id: "B1", risk: "WATCH", color: "#ffd700" },
    { id: "B2", risk: "WARNING", color: "#ff9900" },
    { id: "B3", risk: "WARNING", color: "#ff9900" },

    { id: "C1", risk: "LOW", color: "#00ff88" },
    { id: "C2", risk: "CRITICAL", color: "#ff4444" },
    { id: "C3", risk: "WATCH", color: "#ffd700" }
  ];

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
        AGRICULTURAL THREAT HEATMAP
      </h2>

      <div
        style={{
          color: "#7ddfff",
          fontSize: "13px",
          marginBottom: "20px",
          fontFamily: "monospace"
        }}
      >
        STRATEGIC RISK DISTRIBUTION
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3,1fr)",
          gap: "15px"
        }}
      >
        {sectors.map((sector) => (
          <div
            key={sector.id}
            style={{
              background: `${sector.color}22`,
              border: `1px solid ${sector.color}`,
              borderRadius: "16px",
              padding: "25px",
              textAlign: "center",
              boxShadow: `0 0 20px ${sector.color}33`
            }}
          >
            <div
              style={{
                color: "#c8f8ff",
                fontWeight: "bold",
                marginBottom: "10px"
              }}
            >
              {sector.id}
            </div>

            <div
              style={{
                color: sector.color,
                fontWeight: "bold"
              }}
            >
              {sector.risk}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ThreatHeatmap;