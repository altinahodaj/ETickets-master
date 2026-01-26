import api from "@/libs/api";

export default {
  state: {
    loading: false,
    fetchingActors: false,
    removingActor: false,
    actors: [],
    actor: {},
  },
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value;
    },
    SET_ACTORS(state, payload) {
      state.actors = payload;
    },
    SET_ACTOR(state, payload) {
      state.actor = payload;
    },
    REMOVE_ACTOR(state, id) {
      state.actors = state.actors.filter((h) => h.id !== id);
    },
    ADD_ACTOR(state, payload) {
      state.actors.push(payload);
    },
    UPDATE_ACTOR(state, payload) {
      const index = state.actors.findIndex((a) => a.id === payload.id);
      if (index !== -1) state.actors.splice(index, 1, payload);
      if (state.actor && state.actor.id === payload.id) state.actor = payload;
    },
  },
  actions: {
    getActors({ commit }) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(`actors`)
          .then((response) => {
            commit("SET_ACTORS", response.data.result);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    addActor({ commit }, actor) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .post(`actors`, actor)
          .then((response) => {
            commit("ADD_ACTOR", response.data.result);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    getActor({ commit }, actorId) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(`actors/${actorId}`)
          .then((response) => {
            commit("SET_ACTOR", response.data.result);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    removeActor({ commit }, actorId) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .delete(`actors/${actorId}`)
          .then((response) => {
            commit("REMOVE_ACTOR", actorId);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    editActor({ commit }, actor) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .put(`actors/${actor.id}`, actor)
          .then((response) => {
            commit("UPDATE_ACTOR", response.data.result);
            resolve(response);
          })
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    addActorPhotos({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        const headers = { "Content-Type": "multipart/form-data" };
        api("movies")
          .post(
            `cinemas/${query.cinemaId}/actors/${query.actorId}/photos`,
            query.files,
            { headers }
          )
          .then((response) => resolve(response))
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },

    removeActorPhoto({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .delete(
            `cinemas/${query.cinemaId}/actors/${query.actorId}/photos/${query.photoId}`
          )
          .then((response) => resolve(response))
          .catch((error) => reject(error))
          .finally(() => commit("SET_LOADING", false));
      });
    },
  },
};
