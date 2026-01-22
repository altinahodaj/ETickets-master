export default [
  {
    path: "/register",
    name: "Register",
    meta: {
      layout: "public",
    },
    component: () =>
      import(
        /* webpackChunkName: "register" */ "../../views/Authorization/Register/Register.vue"
      ),
  },
  {
    path: "/login",
    name: "Login",
    meta: {
      layout: "public",
    },
    component: () =>
      import(
        /* webpackChunkName: "login" */ "../../views/Authorization/Login/Login.vue"
      ),
  },
  {
    path: "/profile",
    name: "Profile",
    meta: {
      layout: "public",
    },
    component: () =>
      import(/* webpackChunkName: "login" */ "../../views/Profile.vue"),
  },
  {
    path: "/profile/my-tickets",
    name: "MyTickets",
    meta: {
      layout: "public",
    },
    component: () =>
      import(
        /* webpackChunkName: "login" */ "../../views/UserProfile/MyTickets.vue"
      ),
  },
  {
    path: "/forgotPassword",
    name: "ForgotPassword",
    meta: {
      layout: "public",
    },
    component: () =>
      import(/* webpackChunkName: "login" */ "../../views/ForgotPassword.vue"),
  },

  //Admin Routes
  {
    path: "/admin/users",
    name: "UsersDashboard",
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "login" */ "../../views/Admin/Users/UsersDashboard.vue"
      ),
  },
  {
    path: "/admin/users/create",
    name: "user-create",
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "create-user" */ "../../views/Admin/Users/CreateUser.vue"
      ),
  },
  {
    path: "/admin/users/:userId",
    name: "user-details",
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "user-details" */ "../../views/Admin/Users/UserDetails.vue"
      ),
  },
  {
    path: "/admin/users/edit/:userId",
    name: "user-edit",
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      layout: "dashboard",
    },
    component: () =>
      import(
        /* webpackChunkName: "user-edit" */ "../../views/Admin/Users/EditUser.vue"
      ),
  },
];
