
function AlertCenter({ selectedZone }) {
  const alerts = [
    {
      zone: "PB-04",
      time: "18:45",
      level: "CRITICAL",
      color: "#ff4444",
      message: "PB-04 Moisture Deficit Critical"
    },
    {
      zone: "PB-03",
      time: "18:42",
      level: "WARNING",
      color: "#ffaa00",
      message: "PB-03 Irrigation Required"
    },
    {
      zone: "PB-02",
      time: "18:39",
      level: "WATCH",
      color: "#ffd700",
      message: "PB-02 Emerging Water Stress"
    },
    {
      zone: "PB-01",
      time: "18:36",
      level: "HEALTHY",
      color: "#00ff88",
      message: "PB-01 Operating Normally"
    }
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
          marginBottom: "8px"
        }}
      >
        ALERT CENTER
      </h2>

      <div
        style={{
          color: "#7ddfff",
          fontSize: "13px",
          marginBottom: "20px",
          fontFamily: "monospace"
        }}
      >
        THREAT SURFACE • ACTIVE MONITORING
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: "12px",
          marginBottom: "20px"
        }}
      >
        <div
          style={{
            background: "rgba(0,15,35,0.55)",
            border: "1px solid rgba(0,255,255,0.12)",
            borderRadius: "12px",
            padding: "12px",
            textAlign: "center"
          }}
        >
          <div style={{ color: "#ff4444", fontWeight: "bold" }}>
            2
          </div>
          <div style={{ fontSize: "12px", color: "#9cf6ff" }}>
            CRITICAL
          </div>
        </div>

        <div
          style={{
            background: "rgba(0,15,35,0.55)",
            border: "1px solid rgba(0,255,255,0.12)",
            borderRadius: "12px",
            padding: "12px",
            textAlign: "center"
          }}
        >
          <div style={{ color: "#ffaa00", fontWeight: "bold" }}>
            3
          </div>
          <div style={{ fontSize: "12px", color: "#9cf6ff" }}>
            WARNING
          </div>
        </div>

        <div
          style={{
            background: "rgba(0,15,35,0.55)",
            border: "1px solid rgba(0,255,255,0.12)",
            borderRadius: "12px",
            padding: "12px",
            textAlign: "center"
          }}
        >
          <div style={{ color: "#ffd700", fontWeight: "bold" }}>
            1
          </div>
          <div style={{ fontSize: "12px", color: "#9cf6ff" }}>
            WATCH
          </div>
        </div>

        <div
          style={{
            background: "rgba(0,15,35,0.55)",
            border: "1px solid rgba(0,255,255,0.12)",
            borderRadius: "12px",
            padding: "12px",
            textAlign: "center"
          }}
        >
          <div style={{ color: "#00ff88", fontWeight: "bold" }}>
            8
          </div>
          <div style={{ fontSize: "12px", color: "#9cf6ff" }}>
            HEALTHY
          </div>
        </div>
      </div>

      {alerts.map((alert, index) => (
        <div
          key={index}
          style={{
            marginTop: "12px",
            padding: "16px",
            background:
              alert.zone === selectedZone
                ? `${alert.color}22`
                : "rgba(0,15,35,0.55)",

            boxShadow:
              alert.zone === selectedZone
                ? `0 0 25px ${alert.color}`
                : "none",
            borderLeft: `4px solid ${alert.color}`,
            background: "rgba(0,15,35,0.55)",
            borderRadius: "12px",
            border: "1px solid rgba(0,255,255,0.08)"
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "8px"
            }}
          >
            <div
              style={{
                color: alert.color,
                fontWeight: "bold",
                fontSize: "13px"
              }}
            >
              {alert.level}
            </div>

            <div
              style={{
                color: "#7ddfff",
                fontSize: "12px",
                fontFamily: "monospace"
              }}
            >
              {alert.time}
            </div>
          </div>

          <div
            style={{
              color: "#c8f8ff"
            }}
          >
            {alert.message}
          </div>
        </div>
      ))}
    </div>
  );
}

export default AlertCenter;

