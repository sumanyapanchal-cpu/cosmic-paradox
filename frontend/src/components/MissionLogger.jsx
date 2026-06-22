import { useEffect, useState } from "react";

function MissionLogger({ selectedZone }) {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const now = new Date().toLocaleTimeString();

    setLogs((prev) => [
      {
        time: now,
        message: `${selectedZone} selected`
      },
      ...prev
    ].slice(0, 8));
  }, [selectedZone]);

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
        LIVE MISSION LOG
      </h2>

      {logs.map((log, index) => (
        <div
          key={index}
          style={{
            padding: "12px",
            marginBottom: "10px",
            background: "rgba(0,15,35,0.5)",
            borderRadius: "10px"
          }}
        >
          <div
            style={{
              color: "#7ddfff",
              fontSize: "12px"
            }}
          >
            {log.time}
          </div>

          <div
            style={{
              color: "#c8f8ff"
            }}
          >
            {log.message}
          </div>
        </div>
      ))}
    </div>
  );
}

export default MissionLogger;