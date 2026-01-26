import { getEventsByCinema, getAllEvents } from "@/services/eventsApi";

export default {
  state: {
    loading: false,
    events: [],
  },
  mutations: {
    SET_EVENTS_LOADING(state, v) {
      state.loading = v;
    },
    SET_EVENTS(state, payload) {
      state.events = payload;
    },
  },
  actions: {
    getEventsByCinema({ commit }, cinemaId) {
      commit("SET_EVENTS_LOADING", true);
      return getEventsByCinema(cinemaId)
        .then((res) => {
          commit("SET_EVENTS", res.data.result || []);
          return res;
        })
        .finally(() => commit("SET_EVENTS_LOADING", false));
    },
    getAllEvents({ commit }) {
      commit("SET_EVENTS_LOADING", true);
      return getAllEvents()
        .then((res) => {
          commit("SET_EVENTS", res.data.result || []);
          return res;
        })
        .finally(() => commit("SET_EVENTS_LOADING", false));
    },
  },
};
