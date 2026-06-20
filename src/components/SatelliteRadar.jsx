function SatelliteRadar({ selectedZone }) {
  const radarStyle = `
    @keyframes radarSweep {
      from {
        transform: translate(-50%, -100%) rotate(0deg);
      }

      to {
        transform: translate(-50%, -100%) rotate(360deg);
      }
    }

    @keyframes pulseTarget {
      0% {
        transform: scale(1);
        opacity: 1;
      }

      50% {
        transform: scale(1.4);
        opacity: 0.6;
      }

      100% {
        transform: scale(1);
        opacity: 1;
      }
    }
  `;

  const targets = [
    {
      top: "25%",
      left: "60%",
      color: "#00ff88",
      label: "PB-01",
      status: "TRACKED"
    },
    {
      top: "40%",
      left: "30%",
      color: "#ffd700",
      label: "PB-02",
      status: "WATCH"
    },
    {
      top: "65%",
      left: "55%",
      color: "#ff9900",
      label: "PB-03",
      status: "LOCKED"
    },
    {
      top: "50%",
      left: "80%",
      color: "#ff4444",
      label: "PB-04",
      status: "CRITICAL"
    }
  ];
  return (
    <>
      <style>{radarStyle}</style>

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
          GLOBAL SATELLITE RADAR
        </h2>

        <div
          style={{
            color: "#7ddfff",
            fontSize: "13px",
            marginBottom: "20px",
            fontFamily: "monospace"
          }}
        >
          AGRICULTURAL TARGET ACQUISITION SYSTEM
        </div>

        <div
          style={{
            position: "relative",
            width: "500px",
            height: "500px",
            margin: "auto",
            borderRadius: "50%",
            border: "2px solid rgba(0,255,255,0.25)",
            overflow: "hidden"
          }}
        >
          {/* Radar Rings */}
          {[1, 2, 3, 4].map((ring) => (
            <div
              key={ring}
              style={{
                position: "absolute",
                top: `${ring * 12.5}%`,
                left: `${ring * 12.5}%`,
                width: `${100 - ring * 25}%`,
                height: `${100 - ring * 25}%`,
                borderRadius: "50%",
                border: "1px solid rgba(0,255,255,0.15)"
              }}
            />
          ))}

          {/* Horizontal Line */}
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: 0,
              width: "100%",
              height: "1px",
              background: "rgba(0,255,255,0.2)"
            }}
          />

          {/* Vertical Line */}
          <div
            style={{
              position: "absolute",
              left: "50%",
              top: 0,
              width: "1px",
              height: "100%",
              background: "rgba(0,255,255,0.2)"
            }}
          />

          {/* Radar Sweep */}
          <div
            style={{
              position: "absolute",
              left: "50%",
              top: "50%",
              width: "2px",
              height: "50%",
              background:
                "linear-gradient(to top, rgba(0,255,255,0.05), #00ffff)",
              transformOrigin: "bottom center",
              animation: "radarSweep 4s linear infinite"
            }}
          />

          {/* Center Dot */}
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              width: "10px",
              height: "10px",
              borderRadius: "50%",
              background: "#00ffff",
              transform: "translate(-50%,-50%)",
              boxShadow: "0 0 20px #00ffff"
            }}
          />

          {/* Targets */}
          {targets.map((target) => (
            <div
              key={target.label}
              style={{
                position: "absolute",
                top: target.top,
                left: target.left,
                transform: "translate(-50%,-50%)"
              }}
            >
              <div
                style={{
                  width:
                    target.label === selectedZone
                      ? "22px"
                      : "14px",

                  height:
                    target.label === selectedZone
                      ? "22px"
                      : "14px",

                  borderRadius: "50%",
                  background: target.color,

                  boxShadow:
                    target.label === selectedZone
                      ? `0 0 40px ${target.color}`
                      : `0 0 20px ${target.color}`,

                  animation: "pulseTarget 2s infinite",

                  transition: "all 0.3s ease"
                }}
              />

              <div
                style={{
                  color: target.color,
                  marginTop: "8px",
                  fontSize: "12px",
                  fontWeight: "bold",
                  textAlign: "center"
                }}
              >
                <>
                  <>
                    <div>{target.label}</div>

                    {target.label === selectedZone && (
                      <div
                        style={{
                          fontSize: "10px",
                          color: "#ffffff",
                          marginTop: "3px"
                        }}
                      >
                        ACTIVE TARGET
                      </div>
                    )}
                  </>

                  <div
                    style={{
                      fontSize: "10px",
                      marginTop: "3px"
                    }}
                  >
                    {target.status}
                  </div>
                </>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default SatelliteRadar;