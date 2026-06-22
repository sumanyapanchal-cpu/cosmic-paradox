function MissionStatusBar() {
  const items = [
    {
      label: "SATELLITE STATUS",
      value: "ONLINE",
      color: "#00ff88"
    },
    {
      label: "AI CORE",
      value: "ACTIVE",
      color: "#00ffff"
    },
    {
      label: "GROUND LINK",
      value: "STABLE",
      color: "#ffd700"
    },
    {
      label: "MISSION STATE",
      value: "NOMINAL",
      color: "#00ff88"
    }
  ];

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "repeat(auto-fit,minmax(220px,1fr))",
        gap: "12px",
        marginBottom: "25px"
      }}
    >
      {items.map((item) => (
        <div
          key={item.label}
          style={{
            background: "rgba(10,15,35,0.7)",
            border: "1px solid rgba(0,255,255,0.15)",
            borderRadius: "16px",
            padding: "15px"
          }}
        >
          <div
            style={{
              color: "#7ddfff",
              fontSize: "11px",
              fontFamily: "monospace",
              marginBottom: "6px"
            }}
          >
            {item.label}
          </div>

          <div
            style={{
              color: item.color,
              fontWeight: "bold",
              fontSize: "18px"
            }}
          >
            {item.value}
          </div>
        </div>
      ))}
    </div>
  );
}

export default MissionStatusBar;