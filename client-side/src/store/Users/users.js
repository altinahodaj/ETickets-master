import api from "@/libs/api";

export default {
state: {
loading: true,
loggedIn: false,
error: false,
errorMsg: null,
isAdmin: false,
users: [],
user: null, // ✅ jo {} por null kur s'ka user
},

mutations: {
SET_LOADING(state, value) {
state.loading = value;
},
SET_LOGGED_IN(state, value) {
state.loggedIn = value;
},
SET_ADMIN(state, payload) {
const adminRole = Array.isArray(payload) ? payload.includes(1) : false;
state.isAdmin = adminRole;
},
SET_USERS(state, payload) {
state.users = payload;
},
SET_USER(state, payload) {
state.user = payload; // ✅ këtu e vendosim user-in nga Firebase
},
},

actions: {
getUsers({ commit }) {
commit("SET_LOADING", true);
return new Promise((resolve, reject) => {
api("node")
.get(`users`)
.then((response) => {
commit("SET_USERS", response.data);
resolve(response);
})
.catch((error) => reject(error))
.finally(() => commit("SET_LOADING", false));
});
},

getUser({ commit }, id) {
commit("SET_LOADING", true);
return new Promise((resolve, reject) => {
api("node")
.get(`users/${id}`)
.then((response) => {
commit("SET_USER", response.data);
resolve(response);
})
.catch((error) => reject(error))
.finally(() => commit("SET_LOADING", false));
});
},

makeAdmin({ commit }, id) {
commit("SET_LOADING", true);
return new Promise((resolve, reject) => {
api("node")
.put(`users/${id}/makeAdmin`)
.then((response) => {
commit("SET_USER", response.data);
resolve(response);
})
.catch((error) => reject(error))
.finally(() => commit("SET_LOADING", false));
});
},

removeAdmin({ commit }, id) {
commit("SET_LOADING", true);
return new Promise((resolve, reject) => {
api("node")
.put(`users/${id}/removeAdmin`)
.then((response) => {
commit("SET_USER", response.data);
resolve(response);
})
.catch((error) => reject(error))
.finally(() => commit("SET_LOADING", false));
});
},

addUser({ commit }, query) {
commit("SET_LOADING", true);
return new Promise((resolve, reject) => {
api("node")
.post(`users`, query)
.then((response) => {
commit("SET_USER", response.data.result);
resolve(response);
})
.catch((error) => reject(error))
.finally(() => commit("SET_LOADING", false));
});
},
},
};