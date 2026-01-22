export default [
  {
    path: "/",
    name: "Home",
    meta: {
      layout: "public",
    },
    component: () =>
      import(/* webpackChunkName: "homepage" */ "../../views/HomeView.vue"),
  },
  {
    path: "/home",
    name: "Home",
    meta: {
      layout: "public",
    },
    component: () =>
      import(/* webpackChunkName: "homepage" */ "../../views/HomeView.vue"),
  },
  {
    path: "/aboutus",
    name: "AboutUs",
    meta: {
      layout: "public",
    },
    component: () =>
      import(/* webpackChunkName: "aboutus" */ "../../views/AboutView.vue"),
  },
];
