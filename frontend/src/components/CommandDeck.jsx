function CommandDeck() {
  const commands = [
    "INITIATE SCAN",
    "RUN NDVI ANALYSIS",
    "SYNC SATELLITE",
    "GENERATE REPORT"
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
        SATELLITE COMMAND DECK
      </h2>

      <div
        style={{
          color: "#7ddfff",
          fontSize: "13px",
          marginBottom: "20px",
          fontFamily: "monospace"
        }}
      >
        MISSION OPERATIONS CONTROL
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "15px"
        }}
      >
        {commands.map((command) => (
          <button
            key={command}
            style={{
              background:
                "linear-gradient(135deg,#001b34,#003b5c)",
              color: "#00ffff",
              border:
                "1px solid rgba(0,255,255,0.2)",
              borderRadius: "14px",
              padding: "18px",
              cursor: "pointer",
              fontWeight: "bold",
              fontSize: "14px"
            }}
          >
            {command}
          </button>
        ))}
      </div>
    </div>
  );
}

export default CommandDeck;