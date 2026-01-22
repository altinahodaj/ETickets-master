export default [
  {
    path: "/halls",
    name: "halls",
    meta: {
      layout: "public",
    },
    component: () =>
      import(/* webpackChunkName: "halls" */ "../../views/Halls/Halls.vue"),
  },
  {
    path: "/halls/:id",
    name: "HallDetails",
    component: () =>
      import(
        /* webpackChunkName: "hall-details" */ "../../views/Halls/HallDetails.vue"
      ),
  },

  //Admin Routes
  {
    path: "/admin/halls",
    name: "HallsDashboard",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "halls-dashboard" */ "../../views/Admin/Halls/HallsDashboard.vue"
      ),
  },
  {
    path: "/admin/halls/cinemaId/:cinemaId/create",
    name: "hall-create",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "create-hall" */ "../../views/Admin/Halls/CreateHall.vue"
      ),
  },
  {
    path: "/admin/halls/cinemaId/:cinemaId/:hallId",
    name: "hall-details",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "hall-details" */ "../../views/Admin/Halls/HallDetails.vue"
      ),
  },
  {
    path: "/admin/halls/cinemaId/:cinemaId/edit/:hallId",
    name: "hall-edit",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "edit-hall" */ "../../views/Admin/Halls/EditHall.vue"
      ),
  },
  {
    path: "/admin/halls/cinemaId/:cinemaId/add-photo/:hallId",
    name: "hall-add-photo",
    meta: {
      requiresAuth: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "add-hall-photo" */ "../../views/Admin/Halls/AddHallPhoto.vue"
      ),
  },
];
