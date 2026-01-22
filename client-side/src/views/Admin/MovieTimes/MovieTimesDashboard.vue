<template>
  <div class="table-wrapper p-2 movie-times">
    <v-row>
      <v-col cols="9">
        <h2>Movie Times</h2>
      </v-col>
    </v-row>

    <hr />
    <div class="d-flex mb-5 movie-times-header">
      <div>
        <v-btn color="success" class="mr-2" @click="onCreateMovieTimes()">
          <v-icon left dark> mdi-plus </v-icon>
          Create Movie Times
        </v-btn>
      </div>
      <v-btn
        :loading="loading"
        :disabled="loading"
        color="blue-grey"
        class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
        @click="onRefresh()"
      >
        Refresh
        <v-icon right dark> mdi-refresh </v-icon>
        <template v-slot:loader>
          <span class="custom-loader">
            <v-icon light>mdi-cached</v-icon>
          </span>
        </template>
      </v-btn>
    </div>
    <div class="position-relative d-lg-block">
      <h6>Select Schedule Date:</h6>
      <v-text-field
        class="col-3"
        v-model="todayDate"
        type="datetime-local"
        label="Movie Schedule"
        outlined
        required
      ></v-text-field>
      <v-calendar
        v-if="!loading"
        :events="events"
        :value="todayDate"
        type="day"
        class="mb-4"
      ></v-calendar>
      <hr />
      <v-data-table
        :headers="headers"
        :items="movieTimes"
        item-key="id"
        sort-by="startTime"
        group-by="hallId"
        class="mt-4 elevation-1"
        show-group-by
      >
        <template v-slot:[`item.startTime`]="{ item }">
          <span>
            {{ formatDateTime(item.startTime) }}
          </span>
        </template>
        <template v-slot:[`item.endTime`]="{ item }">
          <span>
            {{ formatDateTime(item.endTime) }}
          </span>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "MovieTimes",
  components: {},
  data() {
    return {
      cinemaId: null,
      movieId: null,
      todayDate: new Date(),
      colors: [
        "blue",
        "indigo",
        "deep-purple",
        "cyan",
        "green",
        "orange",
        "grey darken-1",
      ],
      events: [],
      selected: [],
      headers: [
        {
          text: "Id",
          align: "start",
          sortable: false,
          value: "id",
        },
        { text: "Movie Id", value: "movieId" },
        { text: "Hall Id", value: "hallId" },
        { text: "Start Time", value: "startTime" },
        { text: "End Time", value: "endTime" },
      ],
      fields: [
        { key: "id" },
        { key: "movieId" },
        { key: "hallId" },
        { key: "startTime" },
        { key: "endTime" },
      ],
    };
  },
  computed: {
    loading() {
      return this.$store.state.movieTimes.loading;
    },
    loadingMovies() {
      return this.$store.state.movies.loading;
    },
    movie() {
      return this.$store.state.movies.movie;
    },
    cinema() {
      return this.$store.state.cinemas.cinema;
    },
    movieTimes() {
      return this.$store.state.movieTimes.movieTimes;
    },
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
    this.movieId = this.$route.params.movieId;
    const query = {
      cinemaId: this.cinemaId,
      movieId: this.movieId,
    };
    this.getMovieTimes(query);
  },
  methods: {
    currentDate() {
      const today = new Date();
      const todayToString = `${today}` + "";
      return todayToString;
    },
    onRefresh() {
      this.getMovieTimes({ cinemaId: this.cinemaId, movieId: this.movieId });
    },
    onCreateMovieTimes() {
      this.$router.push({
        name: "movie-times-create",
        params: { cinemaId: this.cinemaId, movieId: this.movieId },
      });
    },
    getMovieTimes(query) {
      this.$store
        .dispatch("getMovieTimes", query)
        .then(() => {
          this.events = [];
          this.movieTimes.forEach((movieTime) => {
            movieTime.startTime = this.formatDateTime(movieTime.startTime);
            movieTime.endTime = this.formatDateTime(movieTime.endTime);
            const event = {
              name: `Schedule ${movieTime.id}`,
              start: this.formatDateTime(movieTime.startTime),
              end: this.formatDateTime(movieTime.endTime),
              color: this.colors[this.rnd(0, this.colors.length - 1)],
              timed: true,
            };
            this.events.push(event);
          });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching movie times!"
          );
        });
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a;
    },
  },
};
</script>
<style lang="scss" scoped></style>
