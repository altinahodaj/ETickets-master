<template>
  <div>
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <h6>Select Schedule Date:</h6>
      {{ selectedDate }}
      <v-text-field
        class="col-3"
        v-model="selectedDate"
        type="datetime-local"
        label="Movie Schedule"
        outlined
        required
      ></v-text-field>
      <v-sheet class="mx-auto" elevation="8">
        <v-sheet
          class="d-flex justify-content-center mx-auto"
          elevation="10"
          max-height="1000"
        >
          <v-slide-group
            class="d-flex justify-content-center ma-2"
            active-class="success"
            show-arrows="always"
          >
            <div v-if="!selectedDateMovieTimes.length > 0">
              <h5>There are no movie schedules at this time.</h5>
            </div>
            <v-slide-item
              v-else
              v-for="movieTime in selectedDateMovieTimes"
              :key="movieTime.id"
              class="mb-2 d-flex justify-content-center"
            >
              <div class="ml-4 mr-4">
                <v-card
                  @click="onDetailsClick(movieTime.id, movieTime.hall.id)"
                  class="p-3 ma-2"
                >
                  <v-row align="center" justify="center">
                    <v-card class="p-2 mx-auto" max-width="300" outlined>
                      <div class="d-flex">
                        <v-icon>confirmation_number</v-icon>
                        <v-list-item three-line>
                          <v-list-item-content>
                            <div class="text-overline mb-4"></div>
                            <v-list-item-title class="text-h5 mb-1">
                              Hall:
                              {{
                                (movieTime.hall && movieTime.hall.name) || "-"
                              }}
                            </v-list-item-title>
                            <v-list-item-subtitle
                              >Start Time:
                              <b>
                                {{ movieScheduleDateTime(movieTime.startTime) }}
                              </b>
                            </v-list-item-subtitle>
                            <v-list-item-subtitle
                              >End Time:
                              <b>
                                {{ movieScheduleDateTime(movieTime.endTime) }}
                              </b>
                            </v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                      </div>
                    </v-card>
                  </v-row>
                </v-card>
              </div>
            </v-slide-item>
          </v-slide-group>
        </v-sheet>
      </v-sheet>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedDate: this.formatShortDateTime(new Date()),
    };
  },
  created() {},
  watch: {
    movie() {
      return this.getMovieTimes();
    },
  },
  computed: {
    loading() {
      return this.$store.state.movieTimes.loading;
    },
    cinema() {
      return this.$store.state.cinemas.cinema;
    },
    movie() {
      return this.$store.state.movies.movie;
    },
    movieTimes() {
      return this.$store.state.movieTimes.movieTimes;
    },
    selectedDateMovieTimes() {
      const movieTimes = this.movieTimes;

      return movieTimes.filter(
        (x) =>
          this.formatSimpleDateTime(x.startTime) ===
          this.formatSimpleDateTime(this.selectedDate)
      );
    },
  },
  methods: {
    onClg() {},
    onDetailsClick(movieTimeId, hallId) {
      this.$router.push({
        name: "MovieTime-Details",
        params: {
          cinemaId: this.cinema.id,
          movieId: this.movie.id,
          hallId,
          movieTimeId: movieTimeId,
        },
      });
    },
  },
};
</script>
