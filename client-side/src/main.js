import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import VueBarcode from "vue-barcode";
import { ensureUserProfile } from "@/firebase/userProfile";

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
apiKey: "AIzaSyBmSyq7Y-QEkF1c5MxEdIhdf2p0a_yiltY",
authDomain: "e-tickets-1871d-2cb76.firebaseapp.com",
projectId: "e-tickets-1871d-2cb76",
storageBucket: "e-tickets-1871d-2cb76.firebasestorage.app",
messagingSenderId: "911479925220",
appId: "1:911479925220:web:4b3e8ea1681eec68f4bff1",
measurementId: "G-E7RMVVM81L",
};

initializeApp(firebaseConfig);

// ✅ Listen Firebase auth state and save user in Vuex
const auth = getAuth();
onAuthStateChanged(auth, async (u) => {
	if (u) {
		store.commit("SET_LOGGED_IN", true);

		// Source of truth for admin: Firebase Auth custom claims
		try {
			const tokenResult = await u.getIdTokenResult();
			const isAdminClaim = Boolean(tokenResult?.claims?.isAdmin);
			store.commit("SET_IS_ADMIN", isAdminClaim);
			console.debug("[auth] loaded token claims", {
				uid: u.uid,
				isAdmin: isAdminClaim,
			});
		} catch (e) {
			store.commit("SET_IS_ADMIN", false);
			console.warn("[auth] failed to load token claims", e);
		}

		// Source of truth: Firestore profile users/{uid} (contains isAdmin)
		try {
			const profile = await ensureUserProfile(u);
			console.debug("[auth] loaded Firestore profile", {
				uid: u.uid,
				email: u.email,
				isAdmin: Boolean(profile?.isAdmin),
			});
			store.commit("SET_USER", profile);
		} catch (e) {
			console.warn("[auth] failed to load Firestore profile; falling back", e);
			// Fallback: keep app working even if Firestore is down
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
		store.commit("SET_IS_ADMIN", false);
		store.commit("SET_LOGGED_IN", false);
	}
});

new Vue({
router,
store,
vuetify,
render: (h) => h(App),
}).$mount("#app");