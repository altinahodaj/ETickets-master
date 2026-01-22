<template>
  <div>
    <nav>
      <v-app-bar color="blue" dark app>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        <v-toolbar-title class="text-uppercase">
          <span>CinemaVerse</span>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu offset-y>
          <template v-slot:activator="{ on }">
            <v-btn text v-on="on">
              <v-icon left>expand_more</v-icon>
              <span>Menu</span>
            </v-btn>
          </template>
          <v-list flat>
            <v-list-item
              v-for="link in links"
              :key="link.text"
              router
              :to="link.route"
              active-class="border"
            >
              <v-list-item-title>{{ link.text }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-btn text :to="{ name: 'Home' }">
          <span>Exit</span>
          <v-icon right>exit_to_app</v-icon>
        </v-btn>
      </v-app-bar>
      <v-navigation-drawer v-model="drawer" dark app class="blue darken-4">
        <v-layout column align-center>
          <v-flex class="mt-5">
            <v-avatar size="100">
              <img :src="user.photoURL" alt="logo" class="logo" />
            </v-avatar>
            <p class="white--text subheading mt-1 text-center">
              {{ user.displayName }}
            </p>
          </v-flex>
          <v-flex class="mt-4 mb-4"> </v-flex>
        </v-layout>
        <v-list flat>
          <v-list-item
            v-for="link in links"
            :key="link.text"
            router
            :to="link.route"
            active-class="border"
          >
            <v-list-item-action>
              <v-icon>{{ link.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ link.text }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </nav>
  </div>
</template>

<script>
export default {
  name: "DashboardLayout",

  props: {
    isLoggedIn: {
      required: true,
      type: Boolean,
    },
    auth: {
      required: true,
    },
  },

  data() {
    return {
      //refactor to get this from firebase auth
      isAdmin: true,
      drawer: true,
      links: [
        {
          icon: "theater_comedy",
          text: "Cinemas",
          route: { name: "CinemasDashboard" },
        },
        {
          icon: "theaters",
          text: "Movies",
          route: { name: "MoviesDashboard" },
        },
        {
          icon: "meeting_room",
          text: "Halls",
          route: { name: "HallsDashboard" },
        },
        {
          icon: "schedule",
          text: "Movie Times",
          route: { name: "MoviesDashboard" },
        },
        { icon: "event", text: "Events", route: { name: "EventsDashboard" } },
        { icon: "group", text: "Actors", route: { name: "ActorsDashboard" } },
        { icon: "person", text: "Users", route: { name: "UsersDashboard" } },
      ],
    };
  },
  computed: {
    user() {
      return this.$store.state.users.user || {};
    },
    loggedIn() {
      return Boolean(this.$store.state.users.loggedIn);
    },
    userProfileLoaded() {
      return this.user && typeof this.user.isAdmin === "boolean";
    },
  },
  created() {
    this.enforceAdminAccess();
  },
  watch: {
    loggedIn() {
      this.enforceAdminAccess();
    },
    userProfileLoaded() {
      this.enforceAdminAccess();
    },
  },
  methods: {
    enforceAdminAccess() {
      if (!this.loggedIn) return;
      if (!this.userProfileLoaded) return;

      if (!this.user.isAdmin) {
        this.$router.push("/");
      }
    },
  },
};
</script>
<style scoped>
.border {
  border-left: 4px solid #0ba518;
}
</style>
