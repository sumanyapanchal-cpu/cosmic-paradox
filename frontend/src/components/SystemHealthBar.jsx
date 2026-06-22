function SystemHealthBar() {
  const items = [
    {
      label: "SATELLITE LINK",
      value: "94%",
      color: "#00ff88"
    },
    {
      label: "AI CORE",
      value: "ONLINE",
      color: "#00ffff"
    },
    {
      label: "GROUND RELAY",
      value: "STABLE",
      color: "#ffd700"
    },
    {
      label: "MISSION STATUS",
      value: "ACTIVE",
      color: "#00ff88"
    }
  ];

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",

        padding: "12px 20px",

        background:
          "rgba(0,15,35,0.9)",

        borderBottom:
          "1px solid rgba(0,255,255,0.15)",

        backdropFilter: "blur(10px)",

        position: "sticky",
        top: 0,
        zIndex: 999
      }}
    >
      {items.map((item) => (
        <div
          key={item.label}
          style={{
            display: "flex",
            gap: "8px",
            alignItems: "center"
          }}
        >
          <div
            style={{
              width: "8px",
              height: "8px",
              borderRadius: "50%",
              background: item.color,
              boxShadow:
                `0 0 10px ${item.color}`
            }}
          />

          <span
            style={{
              color: "#7ddfff",
              fontSize: "12px"
            }}
          >
            {item.label}
          </span>

          <span
            style={{
              color: item.color,
              fontWeight: "bold",
              fontSize: "12px"
            }}
          >
            {item.value}
          </span>
        </div>
      ))}
    </div>
  );
}

export default SystemHealthBar;