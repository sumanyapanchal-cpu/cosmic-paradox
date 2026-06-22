function DemoMode({
  selectedZone,
  setSelectedZone
}) {
  const runDemo = () => {
    const sequence = [
      "PB-01",
      "PB-02",
      "PB-03",
      "PB-04"
    ];

    sequence.forEach((zone, index) => {
      setTimeout(() => {
        setSelectedZone(zone);
      }, index * 2500);
    });
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
          marginBottom: "15px"
        }}
      >
        DEMO MODE
      </h2>

      <button
        onClick={runDemo}
        style={{
          background:
            "linear-gradient(135deg,#00395f,#0077aa)",
          color: "white",
          border: "none",
          padding: "14px 22px",
          borderRadius: "12px",
          cursor: "pointer",
          fontWeight: "bold"
        }}
      >
        START MISSION SIMULATION
      </button>
    </div>
  );
}

export default DemoMode;