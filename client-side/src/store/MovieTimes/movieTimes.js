import api from "@/libs/api";

export default {
  state: {
    loading: false,
    fetchingMovieTimes: false,
    removingMovieTime: false,
    movieTimes: [],
    movieTime: {},
  },
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value;
    },
    SET_MOVIETIMES(state, payload) {
      state.movieTimes = payload;
    },
    SET_MOVIETIME(state, payload) {
      state.movieTime = payload;
    },
    REMOVE_MOVIETIME(state, id) {
      state.movieTimes = state.movieTimes.filter((h) => h.id !== id);
    },
    ADD_MOVIETIME(state, payload) {
      state.movieTimes.push(payload);
    },
  },
  actions: {
    getMovieTimes({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(`cinemas/${query.cinemaId}/movies/${query.movieId}/movie-times`)
          .then((response) => {
            commit("SET_MOVIETIMES", response.data.result);
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
    getMovieTime({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(
            `cinemas/${query.cinemaId}/movies/${query.movieId}/movie-times/${query.movieTimeId}`
          )
          .then((response) => {
            commit("SET_MOVIETIME", response.data.result);
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
    removeMovieTime({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .delete(
            `cinemas/${query.cinemaId}/movies/${query.movieId}/movie-times/${query.movieTimeId}`
          )
          .then((response) => {
            commit("REMOVE_MOVIETIME", query.movieTimeId);
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
    createMovieTime({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .post(
            `cinemas/${query.cinemaId}/movies/${query.movieId}/movie-times`,
            query.movieTime
          )
          .then((response) => {
            commit("ADD_MOVIETIME", query.movieTime);
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
