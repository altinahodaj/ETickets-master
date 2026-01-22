export default [
  {
    path: "/cinemas",
    name: "Cinemas",
    meta: {
      layout: "public",
    },
    component: () =>
      import(
        /* webpackChunkName: "cinemas" */ "../../views/Cinemas/Cinemas.vue"
      ),
  },
  {
    path: "/cinemas/:cinemaId",
    name: "cinema-public-details",
    meta: {
      layout: "public",
    },
    component: () =>
      import(
        /* webpackChunkName: "cinema-public-detials" */ "../../views/Cinemas/CinemaDetails.vue"
      ),
  },
  {
    path: "/admin/cinemas",
    name: "CinemasDashboard",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "cinema-dashboard" */ "../../views/Admin/Cinemas/CinemasDashboard.vue"
      ),
  },
  {
    path: "/admin/cinemas/create",
    name: "cinema-create",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "create-cinema" */ "../../views/Admin/Cinemas/CreateCinema.vue"
      ),
  },
  {
    path: "/admin/cinemas/details/:cinemaId",
    name: "cinema-details",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "cinema-details" */ "../../views/Admin/Cinemas/CinemaDetails.vue"
      ),
  },
  {
    path: "/admin/cinemas/details/:cinemaId/add-photo",
    name: "cinema-add-photo",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "cinema-details" */ "../../views/Admin/Cinemas/AddCinemaPhoto.vue"
      ),
  },
  {
    path: "/admin/cinemas/edit/:cinemaId",
    name: "cinema-edit",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "cinema-details" */ "../../views/Admin/Cinemas/EditCinema.vue"
      ),
  },

  //static pages
  {
    path: "/cinemas/CineplexxPrice",
    name: "CineplexxPrice",
    meta: {
      layout: "public",
    },
    component: () =>
      import(
        /* webpackChunkName: "register" */ "../../components/CinemaPricing.vue"
      ),
  },
];
