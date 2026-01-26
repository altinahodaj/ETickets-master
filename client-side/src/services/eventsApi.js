// src/services/eventsApi.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// 🔹 Merr eventet për një cinema
export const getEventsByCinema = (cinemaId) => {
  return API.get(`/cinemas/${cinemaId}/events`);
};

// 🔹 Merr të gjitha eventet
export const getAllEvents = () => {
  return API.get("/events");
};
