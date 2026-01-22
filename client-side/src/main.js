import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import VueBarcode from "vue-barcode";

import "@/assets/css/style.css";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";

// Global Components
import "./global-components";
// Global Helpers
import helpers from "./helpers/helpers";

import vuetify from "./plugins/vuetify";

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(VueBarcode);

Vue.mixin(helpers);

Vue.config.productionTip = false;

const firebaseConfig = {
apiKey: "AIzaSyBwCfevIeO_qsbJZaeWpJKYQyDTEvLEkz8",
authDomain: "e-tickets-1871d.firebaseapp.com",
projectId: "e-tickets-1871d",
storageBucket: "e-tickets-1871d.appspot.com",
messagingSenderId: "293188362138",
appId: "1:293188362138:web:3b37db09fac9f778d3e423",
};

initializeApp(firebaseConfig);

// ✅ Listen Firebase auth state and save user in Vuex
const auth = getAuth();
onAuthStateChanged(auth, async (u) => {
	if (u) {
		store.commit("SET_LOGGED_IN", true);

		// Prefer the full user profile from Firestore (includes isAdmin)
		try {
			await store.dispatch("getUser", u.uid);
		} catch (e) {
			// Fallback: keep app working even if Node/Firestore is down
			store.commit("SET_USER", {
				id: u.uid,
				displayName: u.displayName || u.email || "User",
				email: u.email || "",
				photoURL: u.photoURL || "",
				isAdmin: false,
			});
		}
	} else {
		store.commit("SET_USER", null);
		store.commit("SET_LOGGED_IN", false);
	}
});

new Vue({
router,
store,
vuetify,
render: (h) => h(App),
}).$mount("#app");