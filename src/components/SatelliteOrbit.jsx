function SatelliteOrbit() {
  return (
    <div
      style={{
        position: "relative",
        width: "250px",
        height: "250px",
        margin: "auto"
      }}
    >
      <div
        style={{
          position: "absolute",
          width: "250px",
          height: "250px",
          border: "1px solid rgba(0,255,255,0.2)",
          borderRadius: "50%"
        }}
      />

      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          width: "14px",
          height: "14px",
          background: "#00ffff",
          borderRadius: "50%",
          transform: "translate(-50%,-50%)",
          boxShadow: "0 0 20px cyan"
        }}
      />

      <div className="satellite"></div>
    </div>
  );
}

export default SatelliteOrbit;