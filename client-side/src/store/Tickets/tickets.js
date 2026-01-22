import api from "@/libs/api";

export default {
  state: {
    loading: false,
    fetchingTickets: false,
    userTickets: [],
    tickets: [],
    ticket: {},
  },
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value;
    },
    SET_TICKETS(state, payload) {
      state.tickets = payload;
    },
    SET_USER_TICKETS(state, payload) {
      state.userTickets = payload;
    },
    SET_TICKET(state, payload) {
      state.ticket = payload;
    },
  },
  actions: {
    getTickets({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(
            `cinemas/${query.cinemaId}/halls/${query.hallId}/movieTimes/${query.movieTimeId}`
          )
          .then((response) => {
            commit("SET_TICKETS", response.data.result);
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
    getUserTickets({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(`cinemas/0/halls/0/user-tickets/${query.userId}`)
          .then((response) => {
            commit("SET_USER_TICKETS", response.data.result);
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
    getTicket({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .get(
            `cinemas/${query.cinemaId}/halls/${query.hallId}/tickets/${query.ticketId}`
          )
          .then((response) => {
            commit("SET_TICKET", response.data.result);
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
    reserveTickets({ commit }, query) {
      commit("SET_LOADING", true);
      return new Promise((resolve, reject) => {
        api("movies")
          .put(
            `cinemas/${query.cinemaId}/halls/${query.hallId}/tickets/movieTimes/${query.movieTimeId}`,
            query.model
          )
          .then((response) => {
            commit("SET_TICKETS", response.data.result);
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
