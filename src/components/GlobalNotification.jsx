import { motion, AnimatePresence } from "framer-motion";

function GlobalNotification({ selectedZone }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={selectedZone}
        initial={{
          opacity: 0,
          x: 100
        }}
        animate={{
          opacity: 1,
          x: 0
        }}
        exit={{
          opacity: 0,
          x: 100
        }}
        transition={{
          duration: 0.4
        }}
        style={{
          position: "fixed",
          top: "20px",
          right: "20px",
          zIndex: 9999,

          background:
            "rgba(0,20,40,0.95)",

          border:
            "1px solid rgba(0,255,255,0.3)",

          borderRadius: "18px",

          padding: "16px 20px",

          boxShadow:
            "0 0 25px rgba(0,255,255,0.15)",

          backdropFilter: "blur(10px)"
        }}
      >
        <div
          style={{
            color: "#7ddfff",
            fontSize: "11px",
            letterSpacing: "2px",
            marginBottom: "6px"
          }}
        >
          MISSION TARGET CHANGED
        </div>

        <div
          style={{
            color: "#00ffff",
            fontWeight: "bold",
            fontSize: "18px"
          }}
        >
          {selectedZone} SELECTED
        </div>
      </motion.div>
    </AnimatePresence>
  );
}

export default GlobalNotification;