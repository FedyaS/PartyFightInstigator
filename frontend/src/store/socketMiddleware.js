// src/store/socketMiddleware.js
import { io } from "socket.io-client";
import {
	updateGameState,
	updatePlayerConversation,
	setLoading,
	setError,
} from "./gameSlice";

const socket = io("http://localhost:5000"); // Your Python backend WebSocket URL

const socketMiddleware = (store) => (next) => (action) => {
	socket.on("connect", () => {
		console.log("Connected to backend");
		store.dispatch(setLoading());
	});

	socket.on("gameUpdate", (data) => {
		store.dispatch(updateGameState(data));
	});

	socket.on("conversationUpdate", (data) => {
		store.dispatch(updatePlayerConversation(data));
	});

	socket.on("disconnect", () => {
		store.dispatch(setError());
	});

	// Emit player message to backend
	if (action.type === "game/sendPlayerMessage") {
		socket.emit("playerMessage", action.payload);
	}

	return next(action);
};

export default socketMiddleware;
