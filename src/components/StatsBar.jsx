function StatsBar() {
  const card = {
    background: "rgba(10,20,40,0.7)",
    border: "1px solid rgba(0,255,255,0.2)",
    borderRadius: "16px",
    padding: "20px",
    textAlign: "center",
    flex: 1
  };

  return (
    <div
      style={{
        display: "flex",
        gap: "20px",
        marginBottom: "40px"
      }}
    >
      <div style={card}>
        <h2 style={{ color: "#00ffff" }}>12</h2>
        <p>Active Satellites</p>
      </div>

      <div style={card}>
        <h2 style={{ color: "#00ffff" }}>84</h2>
        <p>Districts Monitored</p>
      </div>

      <div style={card}>
        <h2 style={{ color: "#00ffff" }}>2.3M</h2>
        <p>Crop Zones</p>
      </div>

      <div style={card}>
        <h2 style={{ color: "#00ffff" }}>92.4%</h2>
        <p>AI Confidence</p>
      </div>
    </div>
  );
}

export default StatsBar;