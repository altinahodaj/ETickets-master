import { getAuth, onAuthStateChanged } from "firebase/auth";
import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store";
import { getUserProfile } from "@/firebase/userProfile";

Vue.use(VueRouter);

// Fix duplicated navigation error (Vue Router 3)
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject)
    return originalPush.call(this, location, onResolve, onReject);
  return originalPush.call(this, location).catch((err) => err);
};

// Route modules (arrays)
import base from "./routes/index";
import users from "./routes/users";
import admin from "./routes/admin";
import movies from "./routes/movies";
import cinemas from "./routes/cinemas";
import event from "./routes/events";
import actors from "./routes/actors";
import halls from "./routes/halls";
import movieTimes from "./routes/movieTimes";

const router = new VueRouter({
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    ...base,
    ...users,
    ...admin,
    ...movies,
    ...cinemas,
    ...event,
    ...actors,
    ...halls,
    ...movieTimes,

    // Login
    {
      path: "/login",
      name: "auth-login",
      component: () => import("@/views/Authorization/Login/Login.vue"),
      meta: {
        isPublic: true,
        layout: "full",
        resource: "Auth",
        redirectIfLoggedIn: true,
      },
    },

    // (optional) 404
    // {
    //   path: "*",
    //   redirect: "/",
    // },
  ],
});

const getCurrentUser = () => {
  return new Promise((resolve, reject) => {
    const removeListener = onAuthStateChanged(
      getAuth(),
      (user) => {
        removeListener();
        resolve(user);
      },
      reject
    );
  });
};

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin);

  if (requiresAuth || requiresAdmin) {
    const user = await getCurrentUser().catch(() => null);

    if (!user) {
      alert("You dont have access!");
      return next("/");
    }

    if (requiresAdmin) {
      // Token-claims are the source of truth for admin
      let isAdmin = Boolean(store.state.users.isAdmin);

      // If role was just changed, force-refresh once to pick up new claims
      if (!isAdmin && typeof user.getIdTokenResult === "function") {
        try {
          const tokenResult = await user.getIdTokenResult(true);
          isAdmin = Boolean(tokenResult?.claims?.isAdmin);
          store.commit("SET_IS_ADMIN", isAdmin);
        } catch (e) {
          // ignore; will fall back to stored value
        }
      }

      // Ensure we have the Firestore-backed profile (contains isAdmin)
      const currentProfileId = store.state.users.user?.id;
      if (!currentProfileId || String(currentProfileId) !== String(user.uid)) {
        try {
          const profile = await getUserProfile(user.uid);
          console.debug("[admin-guard] fetched profile", {
            uid: user.uid,
            hasProfile: Boolean(profile),
            isAdmin: Boolean(profile?.isAdmin),
          });
          if (profile) store.commit("SET_USER", profile);
        } catch (e) {
          console.warn("[admin-guard] failed to fetch profile", e);
        }
      }

      // Prefer claims-based admin flag; fallback to Firestore profile
      const finalIsAdmin = Boolean(
        store.state.users.isAdmin || store.state.users.user?.isAdmin
      );

      console.debug("[admin-guard] computed isAdmin", {
        uid: user.uid,
        storeUserId: store.state.users.user?.id,
        claimsIsAdmin: Boolean(store.state.users.isAdmin),
        profileIsAdmin: Boolean(store.state.users.user?.isAdmin),
        finalIsAdmin,
      });

      if (!finalIsAdmin) {
        alert("Admin access required!");
        return next("/home");
      }
    }
  }

  next();
});

export default router;
