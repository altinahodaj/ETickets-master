import api from "@/libs/api";

export default {
  state: {
    loading: false,
    fetchingHalls: false,
    removingHall: false,
    halls: [],
    hall: {},
  },
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value;
    },
    SET_HALLS(state, payload) {
      state.halls = payload;
    },
    SET_HALL(state, payload) {
      state.hall = payload;
    },
    REMOVE_HALL(state, id) {
      state.halls = state.halls.filter((h) => h.id !== id);
    },
    ADD_HALL(state, payload) {
      state.halls.push(payload);
    },
  },
  actions: {
    getHalls({ commit }, cinemaId) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(`cinemas/${cinemaId}/halls`)
          .then((response) => {
            commit("SET_HALLS", response.data.result);
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
    getHall({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(`cinemas/${query.cinemaId}/halls/${query.hallId}`)
          .then((response) => {
            commit("SET_HALL", response.data.result);
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
    removeHall({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .delete(`cinemas/${query.cinemaId}/halls/${query.hallId}`)
          .then((response) => {
            commit("REMOVE_HALL", query.hallId);
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
    editHall({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .put(`cinemas/${query.cinemaId}/halls/${query.hall.id}`, query.hall)
          .then((response) => {
            commit("ADD_HALL", query.hall);
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
    createHall({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .post(`cinemas/${query.cinemaId}/halls`, query.hall)
          .then((response) => {
            commit("ADD_HALL", query.hall);
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
    addHallPhotos({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        const headers = {
          "Content-Type": "multipart/form-data",
        };
        api("movies")
          .post(
            `cinemas/${query.cinemaId}/halls/${query.hallId}/photos`,
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
    removeHallPhoto({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .delete(
            `cinemas/${query.cinemaId}/halls/${query.hallId}/photos/${query.photoId}`
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
