import GameStats from "./GameStats";
import ConversationView from "./ConversationView";
import ViewSwitcher from "./ViewSwitcher";
import AttendeesView from "./AttendeesView";
// import MapView from "./MapView"; // MAP functionality commented out for now
import "./GameLayout.css";
import { useState } from "react";

function GameLayout({ children }) {
	// const [activeView, setActiveView] = useState("MAP"); // MAP functionality commented out
	const [activeView, setActiveView] = useState("ATTENDEES"); // Always use ATTENDEES view for now
	const [activeNpcId, setActiveNpcId] = useState("ceo");

	return (
		<div className="layout-container">
			<div className="status-bar">
				{/* <h2 className="status-title">Status</h2> */}
				<GameStats /> {/* Added GameStats component */}
			</div>
			<div className="layout-main">
				<ConversationView activeNpcId={activeNpcId} />{" "}
				{/* Added ConversationView component */}
				<aside className="graph-section">
					<ViewSwitcher activeView={activeView} onViewChange={setActiveView} />
					{/* {activeView === "MAP" ? <MapView /> : <AttendeesView />} MAP functionality commented out */}
					<AttendeesView /> {/* Always show AttendeesView for now */}
				</aside>
			</div>
		</div>
	);
}

export default GameLayout;
