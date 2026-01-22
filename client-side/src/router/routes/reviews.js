export default [
  {
    path: "/movies/:movieId/reviews/add",
    name: "AddReview",
    component: () =>
      import(
        /* webpackChunkName: "movie-add-review" */ "../../views/Movie/AddReview.vue"
      ),
  },
];
