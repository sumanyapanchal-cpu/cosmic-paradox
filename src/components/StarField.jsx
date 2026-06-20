function StarField() {
  const stars = Array.from({ length: 150 });

  return (
    <>
      {stars.map((_, i) => (
        <div
          key={i}
          style={{
            position: "fixed",
            width: "2px",
            height: "2px",
            background: "white",
            borderRadius: "50%",
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            opacity: Math.random(),
            pointerEvents: "none"
          }}
        />
      ))}
    </>
  );
}

export default StarField;