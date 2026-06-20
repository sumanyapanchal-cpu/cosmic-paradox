import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

function EventToast({ selectedZone }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    setShow(true);

    const timer = setTimeout(() => {
      setShow(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [selectedZone]);

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{
            opacity: 0,
            y: 50
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          exit={{
            opacity: 0,
            y: 50
          }}
          transition={{
            duration: 0.3
          }}
          style={{
            position: "fixed",
            bottom: "25px",
            right: "25px",

            background:
              "rgba(0,15,35,0.95)",

            border:
              "1px solid rgba(0,255,255,0.2)",

            borderRadius: "16px",

            padding: "16px",

            minWidth: "280px",

            zIndex: 9999,

            boxShadow:
              "0 0 20px rgba(0,255,255,0.15)"
          }}
        >
          <div
            style={{
              color: "#7ddfff",
              fontSize: "12px",
              marginBottom: "6px"
            }}
          >
            [{new Date().toLocaleTimeString()}]
          </div>

          <div
            style={{
              color: "#00ffff",
              fontWeight: "bold"
            }}
          >
            MISSION UPDATE
          </div>

          <div
            style={{
              color: "#c8f8ff",
              marginTop: "8px"
            }}
          >
            Active target switched to {selectedZone}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default EventToast;