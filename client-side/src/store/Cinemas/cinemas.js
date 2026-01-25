import backendApi from "@/services/backendApi";

export default {
  state: {
    loading: false,
    fetchingCinemas: false,
    removingCinema: false,
    cinemas: [],
    cinema: {},
  },
  mutations: {
    SET_CINEMAS_LOADING(state, value) {
      state.loading = value;
    },
    SET_CINEMAS(state, payload) {
      state.cinemas = payload;
    },
    SET_CINEMA(state, payload) {
      state.cinema = payload;
    },
    ADD_CINEMA(state, payload) {
      state.cinemas.push(payload);
    },
    REMOVE_CINEMA(state, id) {
      state.cinemas = state.cinemas.filter((h) => h.id !== id);
    },
  },
  actions: {
    getCinemas({ commit }) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .get("cinemas")
          .then((response) => {
            commit("SET_CINEMAS", response.data.result);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    getCinema({ commit }, cinemaId) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .get(`cinemas/${cinemaId}`)
          .then((response) => {
            commit("SET_CINEMA", response.data.result);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    removeCinema({ commit }, cinemaId) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .delete(`cinemas/${cinemaId}`)
          .then((response) => {
            commit("REMOVE_CINEMA", cinemaId);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    editCinema({ commit }, cinema) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .put(`cinemas/${cinema.id}`, cinema)
          .then((response) => {
            // në kodin tënd origjinal ishte ADD_CINEMA, po e lë siç e kishe
            commit("ADD_CINEMA", cinema);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    createCinema({ commit }, cinema) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .post(`cinemas`, cinema)
          .then((response) => {
            commit("ADD_CINEMA", cinema);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    addCinemaPhotos({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        const headers = { "Content-Type": "multipart/form-data" };

        backendApi
          .post(`cinemas/${query.cinemaId}/photos`, query.files, { headers })
          .then((response) => resolve(response))
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    removeCinemaPhoto({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .delete(`cinemas/${query.cinemaId}/photos/${query.photoId}`)
          .then((response) => resolve(response))
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },
  },
};
