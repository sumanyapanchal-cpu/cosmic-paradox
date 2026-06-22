import { useEffect, useState } from "react";
import { missionData } from "../data/missionData";
import { motion } from "framer-motion";

function AIRecommendationEngine({ selectedZone }) {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);

    const timer = setTimeout(() => {
      setLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, [selectedZone]);

  const data = missionData[selectedZone];

  return (
    <motion.div
      key={selectedZone}
      initial={{
        opacity: 0,
        scale: 0.98
      }}
      animate={{
        opacity: 1,
        scale: 1
      }}
      transition={{
        duration: 0.4
      }}
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
        AI RECOMMENDATION ENGINE
      </h2>

      {loading ? (
        <div
          style={{
            color: "#00ffff",
            fontFamily: "monospace",
            lineHeight: "2"
          }}
        >
          ANALYZING SATELLITE DATA...
          <br />
          PROCESSING NDVI...
          <br />
          GENERATING ADVISORY...
        </div>
      ) : (
        <div>
          <div
            style={{
              color: "#00ff88",
              fontSize: "22px",
              fontWeight: "bold",
              marginBottom: "12px"
            }}
          >
            RECOMMENDATION READY
          </div>

          <div
            style={{
              color: "#c8f8ff",
              lineHeight: "1.8"
            }}
          >
            {data.recommendation}
          </div>

          <div
            style={{
              marginTop: "15px",
              color: "#ffd700",
              fontWeight: "bold"
            }}
          >
            CONFIDENCE: {data.confidence}
          </div>
        </div>
      )}
    </motion.div>
  );
}

export default AIRecommendationEngine;