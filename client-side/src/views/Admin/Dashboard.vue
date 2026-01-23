<template>
  <div class="team">
    <h1 class="subheading grey--text ml-3">Admin Dashboard</h1>
    <v-container>
      <v-layout row wrap>
        <!-- Cinemas Card -->
        <v-flex sm6 xs12 md6 lg3>
          <v-card class="ma-3" hover :to="{ name: 'CinemasDashboard' }">
            <v-list-item>
              <v-list-item-avatar tile class="mt-n7">
                <v-sheet color="green" width="40" height="80" elevation="10">
                  <v-icon dark large>theater_comedy</v-icon>
                </v-sheet>
              </v-list-item-avatar>
              <v-list-item-content>
                <div class="overline text-right">Cinemas</div>
                <v-list-item-title class="headline mb-1 text-right">
                  {{ cinemasCount }}
                </v-list-item-title>
                <div><v-divider></v-divider></div>
              </v-list-item-content>
            </v-list-item>
            <v-card-actions>
              <v-icon text class="ma-2">arrow_forward</v-icon>
              <div class="overline">View Cinemas</div>
            </v-card-actions>
          </v-card>
        </v-flex>

        <!-- Movies Card -->
        <v-flex sm6 xs12 md6 lg3>
          <v-card class="ma-3" hover :to="{ name: 'MoviesDashboard' }">
            <v-list-item>
              <v-list-item-avatar tile class="mt-n7">
                <v-sheet color="#F44336" width="40" height="80" elevation="10">
                  <v-icon dark large>theaters</v-icon>
                </v-sheet>
              </v-list-item-avatar>
              <v-list-item-content>
                <div class="overline text-right">Movies</div>
                <v-list-item-title class="headline mb-1 text-right">
                  {{ moviesCount }}
                </v-list-item-title>
                <div><v-divider></v-divider></div>
              </v-list-item-content>
            </v-list-item>
            <v-card-actions>
              <v-icon text class="ma-2">arrow_forward</v-icon>
              <div class="overline">View Movies</div>
            </v-card-actions>
          </v-card>
        </v-flex>

        <!-- Users Card -->
        <v-flex sm6 xs12 md6 lg3>
          <v-card class="ma-3" hover :to="{ name: 'UsersDashboard' }">
            <v-list-item>
              <v-list-item-avatar tile class="mt-n7">
                <v-sheet color="#03A9F4" width="40" height="80" elevation="10">
                  <v-icon dark large>person</v-icon>
                </v-sheet>
              </v-list-item-avatar>
              <v-list-item-content>
                <div class="overline text-right">Users</div>
                <v-list-item-title class="headline mb-1 text-right">
                  {{ usersCount }}
                </v-list-item-title>
                <div><v-divider></v-divider></div>
              </v-list-item-content>
            </v-list-item>
            <v-card-actions>
              <v-icon text class="ma-2">arrow_forward</v-icon>
              <div class="overline">View Users</div>
            </v-card-actions>
          </v-card>
        </v-flex>

        <!-- Events Card -->
        <v-flex sm6 xs12 md6 lg3>
          <v-card class="ma-3" hover :to="{ name: 'EventsDashboard' }">
            <v-list-item>
              <v-list-item-avatar tile class="mt-n7">
                <v-sheet color="#FFC107" width="40" height="80" elevation="10">
                  <v-icon dark large>event</v-icon>
                </v-sheet>
              </v-list-item-avatar>
              <v-list-item-content>
                <div class="overline text-right">Events</div>
                <v-list-item-title class="headline mb-1 text-right">
                  {{ eventsCount }}
                </v-list-item-title>
                <div><v-divider></v-divider></div>
              </v-list-item-content>
            </v-list-item>
            <v-card-actions>
              <v-icon text class="ma-2">arrow_forward</v-icon>
              <div class="overline">View Events</div>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "AdminDashboard",
  computed: {
    ...mapState({
      cinemasCount: (state) => state.cinemas.cinemas.length,
      moviesCount: (state) => state.movies.movies.length,
      usersCount: (state) => state.users.users.length,
      eventsCount: (state) => state.events.events.length,
    }),
  },
  methods: {
    ...mapActions(["getCinemas", "getMovies", "getUsers", "getEvents"]),
  },
  created() {
    this.getCinemas();
    this.getMovies();
    this.getUsers();
    this.getEvents();
  },
};
</script>
