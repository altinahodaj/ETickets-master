import api from "@/libs/api";

export default {
  state: {
    loading: false,
    fetchingEvents: false,
    removingEvent: false,
    events: [],
    event: {},
  },
  getters: {
    eventList(state) {
      return state.events;
    },
  },
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value;
    },
    SET_EVENTS(state, payload) {
      state.events = payload;
    },
    SET_EVENT(state, payload) {
      state.event = payload;
    },
    REMOVE_EVENT(state, id) {
      state.events = state.events.filter((h) => h.id !== id);
    },
    ADD_EVENT(state, payload) {
      state.events.push(payload);
    },
  },
  actions: {
    getEvents({ commit }, cinemaId) {
      commit("SET_LOADING", true);
      // If no cinemaId, we should ideally have a global endpoint
      // For now, let's try a generic events endpoint if it exists or use a fallback
      const url = cinemaId ? `cinemas/${cinemaId}/events` : `cinemas/1/events/all`;

      return new Promise((resolve, reject) => {
        api("movies")
          .get(url)
          .then((response) => {
        // FastAPI mund të kthejë listën direkt ose të mbështjellë në {result: ...}
        const events = response.data.result !== undefined ? response.data.result : response.data;
        commit("SET_EVENTS", events);
        resolve(response);
      })
      .catch((error) => {
        reject(error);
      })
      .finally(() => {
        commit("SET_LOADING", false);
      });
  });
},

    getEvent({ commit }, query) {
  if (!query?.cinemaId || !query?.eventId) {
    commit("SET_EVENT", {});
    return Promise.resolve({ data: { result: {} } });
  }

  commit("SET_LOADING", true);
  return new Promise((resolve, reject) => {
    api("movies")
      .get(`cinemas/${query.cinemaId}/events/${query.eventId}`)
      .then((response) => {
        const event = response.data.result !== undefined ? response.data.result : response.data;
        commit("SET_EVENT", event);
        resolve(response);
      })
      .catch((error) => {
        reject(error);
      })
      .finally(() => {
        commit("SET_LOADING", false);
      });
  });
},

    removeEvent({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .delete(`cinemas/${query.cinemaId}/events/${query.eventId}`)
          .then((response) => {
            commit("REMOVE_EVENT", query.eventId);
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          })
          .finally(() => {
            commit("SET_LOADING", false);
          });
      });
    },
    editEvent({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .put(
            `cinemas/${query.cinemaId}/events/${query.event.id}`,
            query.event
          )
          .then((response) => {
            commit("ADD_EVENT", query.event);
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          })
          .finally(() => {
            commit("SET_LOADING", false);
          });
      });
    },
    createEvent({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .post(`cinemas/${query.cinemaId}/events`, query.event)
          .then((response) => {
            commit("ADD_EVENT", query.event);
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          })
          .finally(() => {
            commit("SET_LOADING", false);
          });
      });
    },
    goToEvent({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((reject) => {
        api("movies")
          .put(
            `cinemas/${query.cinemaId}/events/IncreaseAttendees/${query.eventId}`,
            query.event
          )
          .catch((error) => {
            reject(error);
          })
          .finally(() => {
            commit("SET_LOADING", false);
          });
      });
    },
    addEventPhotos({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        const headers = {
          "Content-Type": "multipart/form-data",
        };
        api("movies")
          .post(
            `cinemas/${query.cinemaId}/events/${query.eventId}/photos`,
            query.files,
            {
              headers: headers,
            }
          )
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          })
          .finally(() => {
            commit("SET_LOADING", false);
          });
      });
    },
    removeEventPhoto({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .delete(
            `cinemas/${query.cinemaId}/events/${query.eventId}/photos/${query.photoId}`
          )
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          })
          .finally(() => {
            commit("SET_LOADING", false);
          });
      });
    },
  },
};
