import { useEffect, useState } from "react";

function ActivityFeed() {
  const initialLogs = [
    "[22:01] EOS-04 Scan Started",
    "[22:02] NDVI Processing Running",
    "[22:03] Thermal Layer Generated",
    "[22:04] Moisture Analysis Complete",
    "[22:05] PB-03 Stress Detection Triggered",
    "[22:06] AI Advisory Issued",
    "[22:07] Satellite Sync Successful",
    "[22:08] Mission Archive Updated"
  ];
  const [logs, setLogs] = useState(initialLogs);

useEffect(() => {
  const events = [
    "Satellite Link Verified",
    "Crop Health Scan Running",
    "Thermal Layer Updated",
    "Moisture Layer Generated",
    "AI Advisory Generated",
    "District Telemetry Synced",
    "NDVI Pipeline Executed",
    "Mission Archive Updated"
  ];

  const interval = setInterval(() => {
    const time = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit"
    });

    const randomEvent =
      events[Math.floor(Math.random() * events.length)];

    setLogs((prev) => [
      `[${time}] ${randomEvent}`,
      ...prev.slice(0, 11)
    ]);
  }, 4000);

  return () => clearInterval(interval);
}, []);

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
        LIVE SATELLITE ACTIVITY
      </h2>

      <div
        style={{
          color: "#7ddfff",
          fontSize: "13px",
          marginBottom: "20px",
          fontFamily: "monospace"
        }}
      >
        REAL-TIME MISSION OPERATIONS FEED
      </div>

      <div
        style={{
          background: "rgba(0,15,35,0.55)",
          border: "1px solid rgba(0,255,255,0.12)",
          borderRadius: "16px",
          padding: "15px",
          maxHeight: "280px",
          overflowY: "auto",
          fontFamily: "monospace"
        }}
      >
        {logs.map((log, index) => (
          <div
            key={index}
            style={{
              color: "#9cf6ff",
              padding: "10px 0",
              borderBottom:
                index !== logs.length - 1
                  ? "1px solid rgba(0,255,255,0.08)"
                  : "none"
            }}
          >
            {log}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ActivityFeed;