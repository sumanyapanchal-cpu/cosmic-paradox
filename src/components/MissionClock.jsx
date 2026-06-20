import { useEffect, useState } from "react";

function MissionClock() {
  const [time, setTime] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTime((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const hrs = String(
    Math.floor(time / 3600)
  ).padStart(2, "0");

  const mins = String(
    Math.floor((time % 3600) / 60)
  ).padStart(2, "0");

  const secs = String(
    time % 60
  ).padStart(2, "0");

  return (
    <div
      style={{
        textAlign: "center",
        marginTop: "15px",
        color: "#00ffff",
        fontFamily: "monospace",
        fontSize: "20px",
        fontWeight: "bold"
      }}
    >
      T+ {hrs}:{mins}:{secs}
    </div>
  );
}

export default MissionClock;