import { missionData } from "../data/missionData";
import { motion } from "framer-motion";
function MissionBriefing({ selectedZone }) {
  const data = missionData[selectedZone];
  console.log("selectedZone =", selectedZone);
  console.log("data =", missionData[selectedZone]);
  return (
    <motion.div
      key={selectedZone}
      initial={{
        opacity: 0,
        y: 20
      }}
      animate={{
        opacity: 1,
        y: 0
      }}
      transition={{
        duration: 0.4
      }}
      style={{
        background:
          "linear-gradient(135deg, rgba(0,20,40,0.9), rgba(0,10,25,0.95))",
        border: "1px solid rgba(0,255,255,0.25)",
        borderRadius: "28px",
        padding: "35px",
        marginTop: "25px",
        boxShadow:
          "0 0 40px rgba(0,255,255,0.08)",
          backdropFilter: "blur(14px)",
        WebkitBackdropFilter: "blur(14px)",
      }}
    >
      <div
        style={{
          color: "#00ffff",
          fontSize: "14px",
          fontFamily: "monospace",
          marginBottom: "10px",
          letterSpacing: "3px",
          textTransform: "uppercase",
          textShadow: "0 0 12px rgba(0,255,255,0.4)"
        }}
      >
        STRATEGIC MISSION BRIEFING
      </div>

      <h1
        style={{
          color: "#ffffff",
          fontSize: "48px",
          margin: 0,
          marginBottom: "25px"
        }}
      >
        {selectedZone} OPERATIONAL REVIEW
      </h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px"
        }}
      >
        <div>
          <div
            style={{
              color: "#7ddfff",
              fontSize: "12px",
              marginBottom: "8px"
            }}
          >
            THREAT LEVEL
          </div>

          <div
            style={{
              color: "#ff9900",
              fontSize: "28px",
              fontWeight: "bold"
            }}
          >
            {data.threat}
          </div>
        </div>

        <div>
          <div
            style={{
              color: "#7ddfff",
              fontSize: "12px",
              marginBottom: "8px"
            }}
          >
            CONFIDENCE SCORE
          </div>

          <div
            style={{
              color: "#00ffff",
              fontSize: "28px",
              fontWeight: "bold"
            }}
          >
            {data.confidence}
          </div>
        </div>

        <div>
          <div
            style={{
              color: "#7ddfff",
              fontSize: "12px",
              marginBottom: "8px"
            }}
          >
            MISSION STATUS
          </div>

          <div
            style={{
              color: "#00ff88",
              fontSize: "28px",
              fontWeight: "bold"
            }}
          >
            {data.status}
          </div>
        </div>
      </div>

      <div
        style={{
          marginTop: "30px",
          padding: "20px",
          background: "rgba(0,15,35,0.5)",
          borderRadius: "18px",
          border:
            "1px solid rgba(0,255,255,0.1)"
        }}
      >
        <div
          style={{
            color: "#7ddfff",
            marginBottom: "10px",
            fontSize: "12px"
          }}
        >
          AI RECOMMENDATION
        </div>

        <div
          style={{
            color: "#ffffff",
            fontSize: "20px",
            lineHeight: "1.6"
          }}
        >
          {data.recommendation}
        </div>
      </div>
    </motion.div>
  );
}

export default MissionBriefing;