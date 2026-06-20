import SatelliteRadar from "./SatelliteRadar";
import ActivityFeed from "./ActivityFeed";
import AlertCenter from "./AlertCenter";
import MissionStatusBar from "./MissionStatusBar";

function MissionOperationsWall() {
  return (
    <div
      style={{
        marginTop: "25px",
        display: "grid",
        gridTemplateColumns: "2fr 1fr",
        gap: "20px"
      }}
    >
      <div>
        <SatelliteRadar />

        <ActivityFeed />
      </div>

      <div>
        <MissionStatusBar />

        <AlertCenter />
      </div>
    </div>
  );
}

export default MissionOperationsWall;