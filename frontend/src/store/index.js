// src/store/index.js
import { configureStore } from '@reduxjs/toolkit';
import gameReducer from './gameSlice';
import socketMiddleware from './socketMiddleware';

export const store = configureStore({
  reducer: {
    game: gameReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(socketMiddleware),
});