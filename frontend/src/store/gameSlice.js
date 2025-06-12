// src/store/gameSlice.js
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
	time_started: "2025-06-11T01:26:46Z",
	seconds_passed: 0,
	chaos_meter: 50,
	personal_risk: 50,
	goal: "Cause chaos",
	level: "1",
	party_headcount: 13,
	active_rumors: 2,
	status: "LOADING", // 'LOADING', 'PAUSED', 'LIVE', 'WON', 'LOST'
	tick_count: 0,
	notifications: [
		// { id: string, text: string, urgency: 'LOW' | 'MEDIUM' | 'HIGH' }
	],
	npcs: {
		ceo: {
			id: "ceo",
			name: "CEO",
			relationship_score: 25,
			anger: 57,
			personality: "ISTP",
			gullibility: 30,
			conversation_id: null,
			playerConversation: {
				last_npc_message: "Hello! I am the CEO. Ask me anything.",
				last_player_message: null,
				last_message_is: "NPC",
				NPC_is_thinking: false,
			},
		},
		manager: {
			id: "elon",
			name: "Manager",
			relationship_score: 60,
			anger: 20,
			personality: "ENTJ",
			gullibility: 70,
			conversation_id: null,
			playerConversation: {
				last_npc_message: "Hey there! How's the party going?",
				last_player_message: null,
				last_message_is: "NPC",
				NPC_is_thinking: false,
			},
		},
	},
	npcConversations: {
		// id: { id: string, participants: string[], memo: string }
	},
};

const gameSlice = createSlice({
	name: "game",
	initialState,
	reducers: {
		// Backend-driven state updates
		updateGameState: (state, action) => {
			const {
				time_passed,
				chaos_meter,
				personal_risk,
				goal,
				level,
				party_headcount,
				active_rumors,
				status,
				tick_count,
				notifications,
				npcs,
				npcConversations,
			} = action.payload;
			state.time_passed = time_passed ?? state.time_passed;
			state.chaos_meter = chaos_meter ?? state.chaos_meter;
			state.personal_risk = personal_risk ?? state.personal_risk;
			state.goal = goal ?? state.goal;
			state.level = level ?? state.level;
			state.party_headcount = party_headcount ?? state.party_headcount;
			state.active_rumors = active_rumors ?? state.active_rumors;
			state.status = status ?? state.status;
			state.tick_count = tick_count ?? state.tick_count;
			state.notifications = notifications ?? state.notifications;
			state.npcs = npcs ?? state.npcs;
			state.npcConversations = npcConversations ?? state.npcConversations;
		},
		// Frontend-driven: Add new notification
		addNotification: (state, action) => {
			state.notifications.push(action.payload);
		},
		// Frontend-driven: Update player message and set NPC thinking
		sendPlayerMessage: (state, action) => {
			const { npcId, message } = action.payload;
			const npc = state.npcs[npcId];
			if (npc) {
				npc.playerConversation.last_player_message = message;
				npc.playerConversation.last_message_is = "PLAYER";
				npc.playerConversation.NPC_is_thinking = true;
			}
		},
		// Backend-driven: Update NPC conversation state after server response
		updatePlayerConversation: (state, action) => {
			const { npcId, last_npc_message, last_message_is, NPC_is_thinking } =
				action.payload;
			const npc = state.npcs[npcId];
			if (npc) {
				npc.playerConversation.last_npc_message =
					last_npc_message ?? npc.playerConversation.last_npc_message;
				npc.playerConversation.last_message_is =
					last_message_is ?? npc.playerConversation.last_message_is;
				npc.playerConversation.NPC_is_thinking =
					NPC_is_thinking ?? npc.playerConversation.NPC_is_thinking;
			}
		},
		setLoading: (state) => {
			state.status = "LOADING";
		},
		setError: (state) => {
			state.status = "LOST";
		},
	},
});

export const {
	updateGameState,
	addNotification,
	sendPlayerMessage,
	updatePlayerConversation,
	setLoading,
	setError,
} = gameSlice.actions;
export default gameSlice.reducer;
