export default [
	{
		path: "/events",
		name: "Events",
		meta: {
			layout: "public",
		},
		component: () =>
			import(
				/* webpackChunkName: "register" */ "../../views/Events/Events.vue"
			),
	},
	{
		path: "/events/:eventId",
		name: "Event",
		component: () =>
			import(
				/* webpackChunkName: "movie-public-details" */ "../../views/Events/EventDetails.vue"
			),
	},
	{
		path: "/admin/events/cinemaId/:cinemaId/create",
		name: "event-create",
		meta: {
			requiresAuth: true,
			layout: "dashboard",
		},
		component: () =>
			import(
				/* webpackChunkName: "create-event" */ "../../views/Admin/Events/CreateEvent.vue"
			),
	},
	{
		path: "/admin/events/edit/:eventId",
		name: "event-edit",
		meta: {
			requiresAuth: true,
			layout: "dashboard",
		},
		component: () =>
			import(
				/* webpackChunkName: "cinema-details" */ "../../views/Admin/Events/EditEvent.vue"
			),
	},

	{
		path: "/admin/events/cinemaId/:cinemaId/:eventId",
		name: "event-details",
		meta: {
			requiresAuth: true,
			layout: "dashboard",
		},
		component: () =>
			import(
				/* webpackChunkName: "movie-details" */ "../../views/Admin/Events/EventDetails.vue"
			),
	},
	{
		path: "/admin/events/cinemaId/:cinemaId/add-photo/:eventId",
		name: "event-add-photo",
		meta: {
			requiresAuth: true,
			layout: "dashboard",
		},
		component: () =>
			import(
				/* webpackChunkName: "cinema-details" */ "../../views/Admin/Events/AddEventPhoto.vue"
			),
	},
];
