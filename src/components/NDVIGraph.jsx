import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function NDVIGraph() {
  const data = [
    { week: "W1", ndvi: 42 },
    { week: "W2", ndvi: 48 },
    { week: "W3", ndvi: 55 },
    { week: "W4", ndvi: 61 },
    { week: "W5", ndvi: 68 },
    { week: "W6", ndvi: 74 }
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "220px"
      }}
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="week" />
          <YAxis />
          <Tooltip />

          <Line
            type="monotone"
            dataKey="ndvi"
            stroke="#00ffff"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default NDVIGraph;