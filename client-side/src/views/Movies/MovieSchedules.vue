<template>
  <div class="movie-schedules-container">
    <div v-if="loading" class="d-flex justify-center pa-10">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    <div v-else>
      <div class="date-picker-wrapper mb-10">
        <v-row justify="center">
          <v-col cols="12" sm="8" md="4" class="text-center">
            <div class="date-label mb-2">Select Schedule Date:</div>
            <v-text-field
              v-model="selectedDate"
              type="datetime-local"
              label="Movie Schedule"
              outlined
              dense
              hide-details
              prepend-inner-icon="mdi-calendar-clock"
              class="custom-date-field mx-auto"
            ></v-text-field>
          </v-col>
        </v-row>
      </div>

      <div class="schedules-viewport d-flex justify-center">
        <v-slide-group
          active-class="success"
          show-arrows="always"
          class="py-4 centered-slide-group"
        >
          <div v-if="!selectedDateMovieTimes.length" class="no-schedules pa-10 text-center w-100">
            <v-icon size="64" color="grey lighten-1">mdi-clock-alert-outline</v-icon>
            <h5 class="grey--text text--darken-1 mt-4">There are no movie schedules for this date.</h5>
          </div>
          
          <v-slide-item
            v-for="movieTime in selectedDateMovieTimes"
            :key="movieTime.id"
          >
            <v-card
              class="ticket-card ma-6"
              elevation="6"
              @click="onDetailsClick(movieTime)"
            >
              <div class="ticket-left">
                <v-icon color="white" size="36">mdi-movie-open-play</v-icon>
                <div class="text-center mt-1">
                  <div class="ticket-hall-label">HALL</div>
                  <div class="ticket-hall-name">{{ (movieTime.hall && movieTime.hall.name) || "Main Hall" }}</div>
                </div>
              </div>
              
              <div class="ticket-main">
                <v-row no-gutters align="center" class="fill-height">
                  <v-col cols="12" md="8" class="pa-4 d-flex align-center">
                    <div class="ticket-info-wrap">
                      <div class="time-unit">
                        <span class="time-unit-label">STARTS</span>
                        <span class="time-unit-value">{{ movieScheduleDateTime(movieTime.startTime) }}</span>
                      </div>
                      <div class="ticket-divider mx-4"></div>
                      <div class="time-unit">
                        <span class="time-unit-label">ENDS</span>
                        <span class="time-unit-value">{{ movieScheduleDateTime(movieTime.endTime) }}</span>
                      </div>
                    </div>
                  </v-col>
                  
                  <v-col cols="12" md="4" class="fill-height pa-0">
                    <v-btn 
                      block 
                      height="100%"
                      color="primary" 
                      class="book-btn-ticket" 
                      tile
                      elevation="0"
                      @click.stop="onDetailsClick(movieTime)"
                    >
                      <v-icon left>mdi-ticket-confirmation</v-icon>
                      BOOK NOW
                    </v-btn>
                  </v-col>
                </v-row>
              </div>
            </v-card>
          </v-slide-item>
        </v-slide-group>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Përdorim ISO format për datetime-local (yyyy-MM-ddTHH:mm)
      selectedDate: new Date().toISOString().slice(0, 16),
    };
  },
  created() {},
  watch: {
    movie: {
      immediate: true,
      handler(newVal) {
        if (newVal && newVal.id) {
          this.getMovieTimes();
        }
      },
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
      return this.$store.state.movieTimes.movieTimes || [];
    },
    selectedDateMovieTimes() {
      if (!this.movieTimes || !this.selectedDate) return [];

      // We compare only the date part "yyyy-MM-dd"
      const targetDate = this.selectedDate.slice(0, 10);
      
      return this.movieTimes.filter((x) => {
        const startTime = x.startTime || x.start_time;
        if (!startTime) return false;
        return startTime.slice(0, 10) === targetDate;
      });
    },
  },
  methods: {
    getMovieTimes() {
      const query = {
        cinemaId: this.cinema?.id || null,
        movieId: this.movie?.id,
      };
      if (!query.movieId) return;

      this.$store.dispatch("getMovieTimes", query).catch((error) => {
        console.error("Error fetching movie times:", error);
      });
    },
    onClg() {},
    onDetailsClick(movieTime) {
      if (!this.movie || !this.movie.id) {
        console.error("Movie object is missing or invalid:", this.movie);
        return;
      }

      const resolvedHallId =
        movieTime.hallId ||
        movieTime.hall_id ||
        movieTime.hall?.id ||
        movieTime.hall?.hallId ||
        movieTime.hall?.hall_id;

      // Provojmë të nxjerrim cinemaId nga çdo vend i mundshëm
      const movieTime_cId = movieTime.cinemaId || movieTime.cinema_id;
      const movie_cId = this.movie.cinemaId || this.movie.cinema_id;
      const state_cId = this.cinema?.id;
      const route_cId = this.$route.params.cinemaId;

      const cId = movieTime_cId || movie_cId || state_cId || route_cId;

      console.log("--- Navigation Debug ---");
      console.log("MovieTime ID:", movieTime.id);
      console.log("Cinema ID found:", cId);
      console.log("Sources:", { movieTime_cId, movie_cId, state_cId, route_cId });
      console.log("Full movieTime object:", JSON.parse(JSON.stringify(movieTime)));
      console.log("------------------------");

      if (!cId || cId === "undefined") {
        this.errorToast("Missing Cinema ID. Cinema Context: " + (this.cinema?.name || "None"));
        return;
      }

      if (!resolvedHallId || String(resolvedHallId) === "undefined") {
        this.errorToast("Missing Hall ID. Please ensure the movie time has a hall assigned.");
        return;
      }
      
      this.$router.push({
        name: "MovieTime-Details",
        params: {
          cinemaId: String(cId),
          movieId: String(this.movie.id),
          hallId: String(resolvedHallId),
          movieTimeId: String(movieTime.id),
        },
      });
    },
  },
};
</script>

<style scoped>
.movie-schedules-container {
  width: 100%;
}

.date-label {
  font-weight: 700;
  font-size: 16px;
  color: #444;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.custom-date-field {
  max-width: 350px;
}

.centered-slide-group >>> .v-slide-group__content {
  justify-content: center;
}

/* TICKET STYLING */
.ticket-card {
  width: 650px;
  height: 140px;
  display: flex !important;
  flex-direction: row;
  border-radius: 16px !important;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: none;
  background: white;
  cursor: pointer;
}

.ticket-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
}

.ticket-left {
  background: linear-gradient(135deg, #1867c0, #5cb860);
  width: 160px;
  min-width: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  padding: 10px;
}

/* Punch holes effect */
.ticket-left::after, .ticket-left::before {
  content: '';
  position: absolute;
  right: -10px;
  width: 20px;
  height: 20px;
  background-color: #fafafa;
  border-radius: 50%;
  z-index: 2;
}
.ticket-left::before { top: -10px; }
.ticket-left::after { bottom: -10px; }

.ticket-hall-label {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 2px;
  opacity: 0.8;
}

.ticket-hall-name {
  font-size: 18px;
  font-weight: 800;
  text-transform: uppercase;
}

.ticket-main {
  flex-grow: 1;
  background: white;
}

.ticket-info-wrap {
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: space-around;
}

.time-unit {
  display: flex;
  flex-direction: column;
}

.time-unit-label {
  font-size: 11px;
  font-weight: 800;
  color: #bbb;
  letter-spacing: 1px;
}

.time-unit-value {
  font-size: 17px;
  font-weight: 700;
  color: #333;
}

.ticket-divider {
  width: 1px;
  height: 40px;
  background-color: #eee;
}

.book-btn-ticket {
  font-weight: 800 !important;
  letter-spacing: 1px;
  font-size: 16px !important;
  border-left: 2px dashed #eee !important;
}

.no-schedules {
  background: rgba(0,0,0,0.02);
  border-radius: 20px;
  border: 2px dashed #eee;
}

@media (max-width: 768px) {
  .ticket-card {
    width: 320px;
    height: auto;
    flex-direction: column;
  }
  .ticket-left {
    width: 100%;
    height: 80px;
  }
  .ticket-left::before, .ticket-left::after {
    display: none;
  }
  .book-btn-ticket {
    border-left: none !important;
    border-top: 2px dashed #eee !important;
  }
}
</style>
