import GameStats from "./GameStats";
import ConversationView from "./ConversationView";
import ViewSwitcher from "./ViewSwitcher";
import AttendeesView from "./AttendeesView";
import MapView from "./MapView";
import "./GameLayout.css";
import { useState } from "react";

function GameLayout({ children }) {
	const [activeView, setActiveView] = useState("MAP");
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
					{activeView === "MAP" ? <MapView /> : <AttendeesView />}
				</aside>
			</div>
		</div>
	);
}

export default GameLayout;
