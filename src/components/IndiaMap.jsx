function IndiaMap({ selectedZone }) {
  const sectors = [
    {
      id: "PB-01",
      top: "25%",
      left: "35%",
      color: "#00ff88"
    },
    {
      id: "PB-02",
      top: "40%",
      left: "55%",
      color: "#ffd700"
    },
    {
      id: "PB-03",
      top: "60%",
      left: "40%",
      color: "#ff9900"
    },
    {
      id: "PB-04",
      top: "50%",
      left: "75%",
      color: "#ff4444"
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
        background:
          `
  linear-gradient(135deg,#06101f,#0c1c38),
  repeating-linear-gradient(
    0deg,
    transparent,
    transparent 49px,
    rgba(0,255,255,0.03) 50px
  ),
  repeating-linear-gradient(
    90deg,
    transparent,
    transparent 49px,
    rgba(0,255,255,0.03) 50px
  )
  `
      }}
    >
      <h2
        style={{
          color: "#00ffff"
        }}
      >
        INDIA MISSION MAP
      </h2>

      <div
        style={{
          position: "relative",
          height: "500px",
          marginTop: "20px",
          borderRadius: "20px",
          background:
            "linear-gradient(135deg,#06101f,#0c1c38)"
        }}
      >
        {sectors.map((sector) => (
          <div
            key={sector.id}
            style={{
              position: "absolute",
              top: sector.top,
              left: sector.left,
              transform: "translate(-50%,-50%)"
            }}
          >
            <div
              style={{
                width:
                  sector.id === selectedZone
                    ? "28px"
                    : "18px",

                height:
                  sector.id === selectedZone
                    ? "28px"
                    : "18px",

                borderRadius: "50%",
                background: sector.color,

                boxShadow:
                  sector.id === selectedZone
                    ? `0 0 40px ${sector.color}`
                    : `0 0 15px ${sector.color}`,

                transition: "all 0.3s ease"
              }}
            />

            <div
              style={{
                color: sector.color,
                marginTop: "8px",
                fontWeight: "bold",
                fontSize: "12px"
              }}
            >
              {sector.id}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default IndiaMap;