function HolographicEarth() {
  const nodes = [
    { top: "25%", left: "45%", label: "SAT-01" },
    { top: "40%", left: "25%", label: "PB-01" },
    { top: "55%", left: "65%", label: "PB-02" },
    { top: "70%", left: "40%", label: "PB-03" },
    { top: "35%", left: "75%", label: "PB-04" }
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
        HOLOGRAPHIC EARTH NETWORK
      </h2>

      <div
        style={{
          color: "#7ddfff",
          fontSize: "13px",
          marginBottom: "20px",
          fontFamily: "monospace"
        }}
      >
        SATELLITE → GROUND → AGRICULTURE
      </div>

      <div
        style={{
          position: "relative",
          width: "550px",
          height: "550px",
          margin: "auto",
          borderRadius: "50%",
          border: "2px solid rgba(0,255,255,0.2)"
        }}
      >
        {/* Earth Core */}
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            width: "180px",
            height: "180px",
            borderRadius: "50%",
            transform: "translate(-50%,-50%)",
            border: "2px solid #00ffff",
            boxShadow: "0 0 40px rgba(0,255,255,0.3)"
          }}
        />

        {/* Network Nodes */}
        {nodes.map((node) => (
          <div
            key={node.label}
            style={{
              position: "absolute",
              top: node.top,
              left: node.left,
              transform: "translate(-50%,-50%)"
            }}
          >
            <div
              style={{
                width: "14px",
                height: "14px",
                borderRadius: "50%",
                background: "#00ffff",
                boxShadow: "0 0 20px #00ffff"
              }}
            />

            <div
              style={{
                color: "#00ffff",
                marginTop: "8px",
                fontSize: "11px",
                fontWeight: "bold"
              }}
            >
              {node.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HolographicEarth;