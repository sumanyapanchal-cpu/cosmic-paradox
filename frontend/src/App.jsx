import Hero from "./components/Hero";
import MLDashboard from './components/MlDashboard';
import StarField from "./components/StarField";
import CursorGlow from "./components/CursorGlow";
import CommandCenter from "./components/CommandCenter";
import StatsBar from "./components/StatsBar";
import WeatherPanel from "./components/WeatherPanel";
import AlertCenter from "./components/AlertCenter";
import MissionTimeline from "./components/MissionTimeline";
import IndiaMap from "./components/IndiaMap";
import AICopilot from "./components/AICopilot";
import DigitalTwin from "./components/DigitalTwin";
import CommandDeck from "./components/CommandDeck";
import ActivityFeed from "./components/ActivityFeed";
import MissionStatusBar from "./components/MissionStatusBar";
import SatelliteRadar from "./components/SatelliteRadar";
import ThreatHeatmap from "./components/ThreatHeatmap";
import MissionOperationsWall from "./components/MissionOperationsWall";
import AICommandConsole from "./components/AICommandConsole";
import MissionClock from "./components/MissionClock";
import HolographicEarth from "./components/HolographicEarth";
import MissionBriefing from "./components/MissionBriefing";
import AIRecommendationEngine from "./components/AIRecommendationEngine";
import MissionReportCenter from "./components/MissionReportCenter";
import LiveTelemetry from "./components/LiveTelemetry";
import { useState } from "react";
import GlobalNotification from "./components/GlobalNotification";
import ThreatBanner from "./components/ThreatBanner";
import SystemHealthBar from "./components/SystemHealthBar";
import EventToast from "./components/EventToast";
import MissionLogger from "./components/MissionLogger";
import DemoMode from "./components/DemoMode";


function App() {
  const [selectedZone, setSelectedZone] =
    useState("PB-01");
  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "radial-gradient(circle at top, #10254a 0%, #050816 35%, #01040b 100%)",
        overflowX: "hidden",
        paddingBottom: "50px",
        fontFamily:
          "'Inter', 'Segoe UI', sans-serif"
      }}
    >
      <StarField />
      <CursorGlow />

      <Hero />



      <div
        style={{
          width: "90%",
          maxWidth: "1200px",
          margin: "0 auto"
        }}
      >
      

        
        <CommandCenter
          selectedZone={selectedZone}
          setSelectedZone={setSelectedZone}
        />
        <MLDashboard />

        <StatsBar />

        <WeatherPanel />



        <MissionTimeline />

        <IndiaMap
          selectedZone={selectedZone}
        />

        <AICopilot />

        <DigitalTwin
          selectedZone={selectedZone}
        />

        <CommandDeck />
        <AICommandConsole />



        <ThreatHeatmap />
        <MissionOperationsWall />
        <MissionClock />
        <HolographicEarth />
        <MissionBriefing
          selectedZone={selectedZone}
        />
        <SatelliteRadar
          selectedZone={selectedZone}
        />
        <AlertCenter
          selectedZone={selectedZone}
        />
        <AIRecommendationEngine
          selectedZone={selectedZone}
        />
        <MissionReportCenter
          selectedZone={selectedZone}
        />
        <LiveTelemetry />
        <GlobalNotification
          selectedZone={selectedZone}
        />
        <ThreatBanner
          selectedZone={selectedZone}
        />
        <SystemHealthBar />
        <EventToast
          selectedZone={selectedZone}
        />
        <MissionLogger
          selectedZone={selectedZone}
        />
        <DemoMode
          selectedZone={selectedZone}
          setSelectedZone={setSelectedZone}
        />
      </div>
    </div>
  );
}

export default App;