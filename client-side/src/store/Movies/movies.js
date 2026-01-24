import backendApi from "@/services/backendApi";

export default {
  state: {
    loading: false,
    fetchingMovies: false,
    removingMovie: false,
    movieActors: [],
    movies: [],
    movie: {},
  },
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value;
    },
    SET_MOVIE_ACTORS(state, payload) {
      state.movieActors = payload;
    },
    SET_MOVIES(state, payload) {
      state.movies = payload;
    },
    SET_MOVIE(state, payload) {
      state.movie = payload;
    },
    REMOVE_MOVIE(state, id) {
      state.movies = state.movies.filter((h) => h.id !== id);
    },
    ADD_MOVIE(state, payload) {
      state.movies.push(payload);
    },
  },
  actions: {
    getMovies({ commit }, cinemaId) {
  commit("SET_LOADING", true);

  // Nëse nuk ka cinemaId → merr të gjithë filmat (compat/global)
  const url = cinemaId ? `cinemas/${cinemaId}/movies` : `movies`;

  return new Promise((resolve, reject) => {
    backendApi
      .get(url)
      .then((response) => {
        commit("SET_MOVIES", response.data.result || []);
        resolve(response);
      })
      .catch((error) => reject(error))
      .finally(() => commit("SET_LOADING", false));
  });
},


    getMovieActors({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .get(`cinemas/${query.cinemaId}/movies/${query.movieId}/actors`)
          .then((response) => {
            commit("SET_MOVIE_ACTORS", response.data.result);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    getMovie({ commit }, query) {
      commit("SET_LOADING", true);
      
      // Nëse cinemaId është null ose undefined, përdorim rrugën publike
      const url = (!query.cinemaId || query.cinemaId === "null") 
        ? `movies/${query.movieId}` 
        : `cinemas/${query.cinemaId}/movies/${query.movieId}`;

      return new Promise((resolve, reject) => {
        backendApi
          .get(url)
          .then((response) => {
            commit("SET_MOVIE", response.data.result);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    removeMovie({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .delete(`cinemas/${query.cinemaId}/movies/${query.movieId}`)
          .then((response) => {
            commit("REMOVE_MOVIE", query.movieId);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    editMovie({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .put(`cinemas/${query.cinemaId}/movies/${query.movie.id}`, query.movie)
          .then((response) => {
            commit("ADD_MOVIE", query.movie);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    createMovie({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .post(`cinemas/${query.cinemaId}/movies`, query.movie)
          .then((response) => {
            commit("ADD_MOVIE", query.movie);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    addMoviePhotos({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        const headers = { "Content-Type": "multipart/form-data" };

        backendApi
          .post(
            `cinemas/${query.cinemaId}/movies/${query.movieId}/photos`,
            query.files,
            { headers }
          )
          .then((response) => resolve(response))
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    removeMoviePhoto({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        backendApi
          .delete(
            `cinemas/${query.cinemaId}/movies/${query.movieId}/photos/${query.photoId}`
          )
          .then((response) => resolve(response))
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },
  },
};
