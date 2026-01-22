<template>
  <div>
    <UpcomingMovies />
    <section id="features" class="grey lighten-3">
      <div class="py-12"></div>
      <v-container class="text-center">
        <h2 class="display-2 font-weight-bold mb-3">CINEMAVERSE FEATURES</h2>

        <v-responsive class="mx-auto mb-12" width="56">
          <v-divider class="mb-1"></v-divider>

          <v-divider></v-divider>
        </v-responsive>

        <v-row>
          <v-col
            v-for="({ icon, title, text }, i) in features"
            :key="i"
            cols="12"
            md="4"
          >
            <v-card class="py-12 px-4" color="grey lighten-5" flat>
              <v-theme-provider dark>
                <div>
                  <v-avatar color="primary" size="88">
                    <v-icon large v-text="icon"></v-icon>
                  </v-avatar>
                </div>
              </v-theme-provider>

              <v-card-title
                class="justify-center font-weight-black text-uppercase"
                v-text="title"
              ></v-card-title>

              <v-card-text class="subtitle-1" v-text="text"> </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <div class="py-12"></div>
    </section>
    <section id="stats">
      <v-parallax
        :height="$vuetify.breakpoint.smAndDown ? 700 : 500"
        src="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
      >
        <v-container fill-height>
          <v-row class="mx-auto">
            <v-col
              v-for="[value, title] of stats"
              :key="title"
              cols="12"
              md="3"
            >
              <div class="text-center">
                <div
                  class="display-3 font-weight-black mb-4"
                  v-text="value"
                ></div>
                <div
                  class="title font-weight-regular text-uppercase"
                  v-text="title"
                ></div>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-parallax>
    </section>
    <div style="margin-top: 60px; margin-bottom: 60px">
      <h1 class="container d-flex justify-content-center">Available Movies</h1>
      <v-sheet
        class="d-flex justify-content-center mx-auto"
        elevation="10"
        max-height="1000"
      >
        <v-slide-group
          v-model="model"
          class="d-flex justify-content-center pa-4 ma-2"
          active-class="success"
          show-arrows="always"
        >
          <v-slide-item
            v-for="movie in movies"
            :key="movie.id"
            v-slot="{ toggle }"
            style="margin-top: 20px; margin-bottom: 20px"
            class="d-flex justify-content-center"
          >
            <div class="ml-2 mr-2">
              <v-card @click="toggle">
                <v-row align="center" justify="center">
                  <movie-card
                    style="margin: 60px"
                    :hideDetails="true"
                    :movie="movie"
                  />
                </v-row>
              </v-card>
            </div>
          </v-slide-item>
        </v-slide-group>
      </v-sheet>
    </div>
    <div style="margin-top: 60px; margin-bottom: 60px">
      <h1 class="container d-flex justify-content-center">Events</h1>
      <v-sheet
        class="d-flex justify-content-center mx-auto"
        elevation="10"
        max-height="1000"
      >
        <v-slide-group
          v-model="model"
          class="d-flex justify-content-center pa-4 ma-2"
          active-class="success"
          show-arrows
        >
          <v-slide-item
            v-for="event in events"
            :key="event.id"
            v-slot="{ toggle }"
            style="margin-top: 20px; margin-bottom: 20px"
            class="d-flex justify-content-center"
          >
            <div class="ml-2 mr-2">
              <v-card @click="toggle">
                <v-row align="center" justify="center">
                  <EventCardPhoto style="margin: 60px" :event="event" />
                </v-row>
              </v-card>
            </div>
          </v-slide-item>
        </v-slide-group>
      </v-sheet>
    </div>

    <!-- <div>
			<h1 class="text-center">Events</h1>
			<EventCardPhoto :event="events[0]" />
		</div> -->

    <v-divider></v-divider>

    <v-divider></v-divider>
    <div>
      <Welcome />
    </div>
    <v-divider></v-divider>
    <v-divider></v-divider>
    <div>
      <Social />
      <!-- <Subscribe /> -->
    </div>
  </div>
</template>

<script>
import UpcomingMovies from "../components/SlideshowMovies.vue";
import Social from "../components/Social.vue";
import Welcome from "../components/Welcome.vue";
import MovieCard from "@/components/cards/MovieCard.vue";
import EventCardPhoto from "@/components/EventCardPhoto.vue";

export default {
  name: "Home",
  components: {
    MovieCard,
    UpcomingMovies,
    Social,
    Welcome,
    EventCardPhoto,
  },
  data() {
    return {
      cinemaId: null,
      stats: [
        ["1500+", "Tickets Sold"],
        ["145+", "Movies Streamed"],
        ["2300+", "Visits"],
        ["500+", "Events"],
      ],
      features: [
        {
          icon: "mdi-account-group-outline",
          title: "Vibrant Community",
          text: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Iusto cupiditate sint possimus quidem atque harum excepturi nemo velit tempora! Enim inventore fuga, qui ipsum eveniet facilis obcaecati corrupti asperiores nam",
        },
        {
          icon: "mdi-update",
          title: "Frequent Updates",
          text: "Sed ut elementum justo. Suspendisse non justo enim. Vestibulum cursus mauris dui, a luctus ex blandit. Lorem ipsum dolor sit amet consectetur adipisicing elit. qui ipsum eveniet facilis obcaecati corrupti consectetur adipisicing elit.",
        },
        {
          icon: "mdi-shield-outline",
          title: "Long-term Support",
          text: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Iusto cupiditate sint possimus quidem atque harum excepturi nemo velit tempora! Enim inventore fuga, qui ipsum eveniet facilis obcaecati corrupti asperiores nam",
        },
      ],
      model: null,
    };
  },
  watch: {
    cinema() {
      return this.getMovies();
    },
  },
  created() {
    this.getCinemas();
    this.getMovies();
    this.getEvents();
  },
  computed: {
    movies() {
      return this.$store.state.movies.movies;
    },
    cinemas() {
      return this.$store.state.cinemas.cinemas;
    },
    cinema() {
      return this.$store.state.cinemas.cinema;
    },
    user() {
      return this.$store.state.users.user;
    },
    events() {
      return this.$store.state.events.events;
    },
  },
  methods: {
    getCinemas() {
      this.$store.dispatch("getCinemas").catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching cinemas!"
        );
      });
    },
    getMovies() {
      this.$store
        .dispatch(
          "getMovies",
          this.cinemaId == null ? this.cinema.id : this.cinemaId
        )
        .then(() => {})
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching movies!"
          );
        });
    },
    getEvents() {
      this.$store
        .dispatch(
          "getEvents",
          this.cinemaId == null ? this.cinema.id : this.cinemaId
        )
        .catch((error) => {
          console.log(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching events!"
          );
        });
    },
  },
  props: {},
};
</script>

<style scoped></style>
