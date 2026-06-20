import { useState } from "react";

function CursorGlow() {
  const [position, setPosition] = useState({
    x: window.innerWidth / 2,
    y: window.innerHeight / 2
  });

  return (
    <div
      onMouseMove={(e) =>
        setPosition({
          x: e.clientX,
          y: e.clientY
        })
      }
      style={{
        position: "fixed",
        inset: 0,
        pointerEvents: "none",
        zIndex: 1
      }}
    >
      <div
        style={{
          position: "absolute",
          left: position.x - 150,
          top: position.y - 150,
          width: "300px",
          height: "300px",
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(0,255,255,0.18), transparent 70%)",
          transition: "all 0.08s linear"
        }}
      />
    </div>
  );
}

export default CursorGlow;