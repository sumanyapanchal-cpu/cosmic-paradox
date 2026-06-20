function WeatherPanel() {
  const panelStyle = {
    background: "rgba(10,15,35,0.7)",
    border: "1px solid rgba(0,255,255,0.2)",
    borderRadius: "24px",
    padding: "25px",
    marginTop: "25px"
  };

  const cards = [
    {
      title: "TEMPERATURE",
      value: "34°C",
      color: "#ff9966"
    },
    {
      title: "HUMIDITY",
      value: "62%",
      color: "#00ffff"
    },
    {
      title: "RAIN PROBABILITY",
      value: "18%",
      color: "#00ff88"
    },
    {
      title: "SATELLITE LINK",
      value: "94%",
      color: "#ffd700"
    }
  ];

  return (
    <div style={panelStyle}>
      <h2
        style={{
          color: "#00ffff",
          marginBottom: "8px"
        }}
      >
        WEATHER INTELLIGENCE
      </h2>

      <div
        style={{
          color: "#7ddfff",
          fontSize: "13px",
          marginBottom: "20px",
          fontFamily: "monospace"
        }}
      >
        ATMOSPHERIC TELEMETRY • PUNJAB THEATER
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(180px,1fr))",
          gap: "15px"
        }}
      >
        {cards.map((card, index) => (
          <div
            key={index}
            style={{
              background: "rgba(0,15,35,0.55)",
              border:
                "1px solid rgba(0,255,255,0.12)",
              borderRadius: "16px",
              padding: "18px",
              boxShadow:
                "0 0 20px rgba(0,255,255,0.05)"
            }}
          >
            <div
              style={{
                color: "#7ddfff",
                fontSize: "12px",
                marginBottom: "10px",
                fontFamily: "monospace"
              }}
            >
              {card.title}
            </div>

            <div
              style={{
                color: card.color,
                fontSize: "28px",
                fontWeight: "bold"
              }}
            >
              {card.value}
            </div>
          </div>
        ))}
      </div>

      <div
        style={{
          marginTop: "20px",
          background: "rgba(0,15,35,0.55)",
          border:
            "1px solid rgba(0,255,255,0.12)",
          borderRadius: "16px",
          padding: "16px"
        }}
      >
        <div
          style={{
            color: "#7ddfff",
            fontSize: "12px",
            marginBottom: "8px",
            fontFamily: "monospace"
          }}
        >
          WEATHER THREAT INDEX
        </div>

        <div
          style={{
            display: "flex",
            gap: "10px"
          }}
        >
          <div
            style={{
              background: "#00ff88",
              color: "#001018",
              padding: "6px 12px",
              borderRadius: "8px",
              fontWeight: "bold"
            }}
          >
            LOW
          </div>

          <div
            style={{
              color: "#ffd700",
              padding: "6px 12px"
            }}
          >
            MEDIUM
          </div>

          <div
            style={{
              color: "#ff9966",
              padding: "6px 12px"
            }}
          >
            HIGH
          </div>

          <div
            style={{
              color: "#ff5555",
              padding: "6px 12px"
            }}
          >
            CRITICAL
          </div>
        </div>
      </div>
    </div>
  );
}

export default WeatherPanel;

