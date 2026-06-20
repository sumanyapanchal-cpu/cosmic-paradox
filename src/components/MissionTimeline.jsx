function MissionTimeline() {
  const logs = [
  { time: "18:31", type: "SCAN", message: "EOS-04 Satellite Pass Detected" },
  { time: "18:33", type: "SCAN", message: "Sentinel-2 Data Acquired" },
  { time: "18:35", type: "ANALYSIS", message: "NDVI Processing Started" },
  { time: "18:36", type: "ANALYSIS", message: "Vegetation Index Computed" },
  { time: "18:37", type: "COMPLETE", message: "Moisture Layer Generated" },
  { time: "18:38", type: "COMPLETE", message: "Crop Stress Detection Complete" },
  { time: "18:39", type: "ADVISORY", message: "PB-02 Irrigation Review Suggested" },
  { time: "18:40", type: "SCAN", message: "Thermal Data Synced" },
  { time: "18:41", type: "SCAN", message: "Sentinel-2 Scan Started" },
  { time: "18:42", type: "ANALYSIS", message: "NDVI Processing Initiated" },
  { time: "18:43", type: "COMPLETE", message: "Moisture Analysis Complete" },
  { time: "18:44", type: "ADVISORY", message: "AI Advisory Generated" },
  { time: "18:45", type: "ARCHIVED", message: "Mission Archived" }
];

  const getColor = (type) => {
    switch (type) {
      case "SCAN":
        return "#00ffff";
      case "ANALYSIS":
        return "#00bfff";
      case "COMPLETE":
        return "#00ff88";
      case "ADVISORY":
        return "#ffd700";
      case "ARCHIVED":
        return "#ff6666";
      default:
        return "#00ffff";
    }
  };

  return (
    <div
      style={{
  background: "rgba(0,15,35,0.55)",
  border: "1px solid rgba(0,255,255,0.12)",
  boxShadow: "0 0 20px rgba(0,255,255,0.05)",
  padding: "12px",
  borderRadius: "12px",
  textAlign: "center"
}}
    >
      <h2
        style={{
          color: "#00ffff",
          marginBottom: "20px"
        }}
      >
        MISSION TIMELINE
      </h2>
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
  boxShadow: "0 0 20px rgba(0,255,255,0.05)",
  padding: "12px",
  borderRadius: "12px",
  textAlign: "center"
}}
  >
    <div style={{ color: "#00ffff", fontWeight: "bold" }}>
      12
    </div>
    <div style={{ fontSize: "12px", color: "#9cf6ff" }}>
      ACTIVE MISSIONS
    </div>
  </div>

  <div
    style={{
      background: "rgba(0,15,35,0.55)",
      border: "1px solid rgba(0,255,255,0.12)",
      boxShadow: "0 0 20px rgba(0,255,255,0.05)",
      padding: "12px",
      borderRadius: "12px",
      textAlign: "center"
    }}
  >
    <div style={{ color: "#00ff88", fontWeight: "bold" }}>
      7
    </div>
    <div style={{ fontSize: "12px", color: "#9cf6ff" }}>
      SATELLITE PASSES
    </div>
  </div>

  <div
    style={{
      background: "rgba(0,15,35,0.55)",
      border: "1px solid rgba(0,255,255,0.12)",
      boxShadow: "0 0 20px rgba(0,255,255,0.05)",
      padding: "12px",
      borderRadius: "12px",
      textAlign: "center"
    }}
  >
    <div style={{ color: "#ffd700", fontWeight: "bold" }}>
      24
    </div>
    <div style={{ fontSize: "12px", color: "#9cf6ff" }}>
      ADVISORIES
    </div>
  </div>

  <div
    style={{
      background: "rgba(0,15,35,0.55)",
      border: "1px solid rgba(0,255,255,0.12)",
      boxShadow: "0 0 20px rgba(0,255,255,0.05)",
      padding: "12px",
      borderRadius: "12px",
      textAlign: "center"
    }}
  >
    <div style={{ color: "#00ffff", fontWeight: "bold" }}>
      98.7%
    </div>
    <div style={{ fontSize: "12px", color: "#9cf6ff" }}>
      SYSTEM HEALTH
    </div>
  </div>
</div>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "12px",
          maxHeight: "420px",
          overflowY: "auto",
          paddingRight: "8px"
        }}
      >
        {logs.map((log, index) => (
            
          <div
            key={index}
            style={{
              display: "flex",
              gap: "15px",
              alignItems: "flex-start"
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center"
              }}
            >
              <div
                style={{
                  width: "12px",
                  height: "12px",
                  borderRadius: "50%",
                  background: getColor(log.type),
                  boxShadow: `0 0 15px ${getColor(log.type)}`
                }}
              />

              {index !== logs.length - 1 && (
                <div
                  style={{
                    width: "2px",
                    height: "50px",
                    background: "rgba(0,255,255,0.3)"
                  }}
                />
              )}
            </div>

            <div
              style={{
                flex: 1,
                background: "rgba(0,15,35,0.55)",
                border: "1px solid rgba(0,255,255,0.12)",
                borderRadius: "12px",
                padding: "14px",
                color: "#9cf6ff",
                fontFamily: "monospace"
              }}
            >
              <div
                style={{
                  color: getColor(log.type),
                  fontSize: "12px",
                  fontWeight: "bold",
                  marginBottom: "6px"
                }}
              >
                [{log.type}]
              </div>

              <div>
                [{log.time}] {log.message}
              </div>
            </div>
          </div>
        ))}
        
      </div>
    </div>
  );
}

export default MissionTimeline;