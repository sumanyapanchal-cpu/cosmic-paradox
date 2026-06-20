import { motion, AnimatePresence } from "framer-motion";

function ThreatBanner({ selectedZone }) {
  const isCritical =
    selectedZone === "PB-04";

  return (
    <AnimatePresence>
      {isCritical && (
        <motion.div
          initial={{
            opacity: 0,
            y: -50
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          exit={{
            opacity: 0,
            y: -50
          }}
          transition={{
            duration: 0.4
          }}
          style={{
            background:
              "linear-gradient(90deg,#400000,#880000)",

            border:
              "1px solid rgba(255,80,80,0.5)",

            padding: "14px",

            textAlign: "center",

            color: "white",

            fontWeight: "bold",

            letterSpacing: "2px",

            marginBottom: "20px",

            boxShadow:
              "0 0 25px rgba(255,0,0,0.35)"
          }}
        >
          🚨 CRITICAL MOISTURE THREAT DETECTED
          — PB-04 REQUIRES IMMEDIATE ACTION
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default ThreatBanner;