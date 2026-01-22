export default [
  {
    path: "/movies",
    name: "Movies",
    meta: {
      layout: "public",
    },
    component: () =>
      import(
        /* webpackChunkName: "register" */ "../../views/Movies/Movies.vue"
      ),
  },
  {
    path: "/tickets",
    name: "Tickets",
    meta: {
      layout: "public",
    },
    component: () =>
      import(
        /* webpackChunkName: "register" */ "../../views/Movies/Tickets.vue"
      ),
  },
  {
    path: "/seats",
    name: "Seats",
    meta: {
      layout: "public",
    },
    component: () =>
      import(/* webpackChunkName: "register" */ "../../views/Movies/Seats.vue"),
  },
  {
    path: "/movies/:movieId",
    name: "Movie",
    component: () =>
      import(
        /* webpackChunkName: "movie-public-details" */ "../../views/Movies/MovieDetails.vue"
      ),
  },

  //Admin Routes
  {
    path: "/admin/movies",
    name: "MoviesDashboard",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "movies-dashboard" */ "../../views/Admin/Movies/MoviesDashboard.vue"
      ),
  },
  {
    path: "/admin/movies/cinemaId/:cinemaId/create",
    name: "movie-create",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "create-movie" */ "../../views/Admin/Movies/CreateMovie.vue"
      ),
  },
  {
    path: "/admin/movies/cinemaId/:cinemaId/:movieId",
    name: "movie-details",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "movie-details" */ "../../views/Admin/Movies/MovieDetails.vue"
      ),
  },
  {
    path: "/admin/movies/cinemaId/:cinemaId/edit/:movieId",
    name: "movie-edit",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "movie-details" */ "../../views/Admin/Movies/EditMovie.vue"
      ),
  },
  {
    path: "/admin/movies/cinemaId/:cinemaId/add-photo/:movieId",
    name: "movie-add-photo",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "cinema-details" */ "../../views/Admin/Movies/AddMoviePhoto.vue"
      ),
  },
];
