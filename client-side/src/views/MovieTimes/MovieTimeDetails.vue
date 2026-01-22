<template>
  <div>
    <div v-if="loading"><loading-page /></div>
    <div v-else class="d-flex justify-content-between m-auto flex-wrap">
      <div class="cinema-map col-12 col-lg-9">
        <div class="d-flex justify-content-center align-center">
          <h1>{{ hall.name }}</h1>
        </div>
        <div class="mt-5 bg-dark d-flex justify-content-center">
          <h1 class="text-light">
            <span class="material-icons"> desktop_windows </span> Screen
            <span class="material-icons"> desktop_windows </span>
          </h1>
        </div>
        <div class="mt-10 w-100">
          <div
            v-for="row in hall.rows"
            :key="row.id"
            class="d-flex justify-content-center w-100"
          >
            <div
              v-for="seat in row.seats"
              :key="seat.id"
              :class="row.isVipRow ? 'm-3' : 'm-1'"
            >
              <v-btn
                v-if="seat.isVipSeat"
                :disabled="!seat.ticket.isAvailable || hasEnded"
                @click="selectSeat(seat)"
                :color="isSeatSelected(seat) ? 'green' : 'orange'"
              >
                <div
                  v-if="seat.isSeatForCouple"
                  v-b-tooltip.hover
                  title="VIP Couple Seat"
                >
                  <span><v-icon color="white" small>favorite</v-icon></span>
                  <span>
                    <v-icon color="white" large>weekend </v-icon>
                  </span>
                  <span><v-icon color="white" small>favorite</v-icon></span>
                </div>
                <v-icon
                  v-else
                  v-b-tooltip.hover
                  title="VIP Seat"
                  color="white"
                  large
                  >chair</v-icon
                >
              </v-btn>
              <v-btn
                :disabled="!seat.ticket.isAvailable || hasEnded"
                v-else
                depressed
                @click="selectSeat(seat)"
                :color="isSeatSelected(seat) ? 'green' : 'primary'"
              >
                <div
                  v-if="seat.isSeatForCouple"
                  v-b-tooltip.hover
                  title="Couple Seat"
                >
                  <span><v-icon color="white" small>favorite</v-icon></span>
                  <span>
                    <v-icon color="white" large>weekend </v-icon>
                  </span>
                  <span><v-icon color="white" small>favorite</v-icon></span>
                </div>
                <v-icon
                  v-else
                  v-b-tooltip.hover
                  title="Normal Seat"
                  color="white"
                  large
                >
                  event_seat
                </v-icon>
              </v-btn>
            </div>
          </div>
        </div>
      </div>
      <div class="checkout col-12 col-lg-3">
        <h1>Checkout</h1>
        <v-card class="mx-auto" tile>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                >Total Tickets:
                <b>{{ selectedSeats.length }}</b></v-list-item-title
              >
              <v-list-item-subtitle>
                {{ selectedSeats.seatName }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title
                >Price:
                <b
                  >{{ parseFloat(totalPrice).toFixed(2) }}€</b
                ></v-list-item-title
              >
              <v-list-item-subtitle>
                <b>Cash</b> is the only payment method currently.
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title
                >Tax:
                <b
                  >{{ parseFloat(totalPrice * 0.18).toFixed(2) }}€</b
                ></v-list-item-title
              >
              <v-list-item-subtitle>
                <b>18% TVSH</b> is added on top of each ticket.
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <hr />
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title
                ><h2>
                  Total:
                  {{ parseFloat(totalPrice + totalPrice * 0.18).toFixed(2) }}€
                </h2></v-list-item-title
              >
              <v-list-item-subtitle>
                Ticket will be reserved for:
                <b>{{ currentUser.displayName }}</b
                >.
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item three-line v-if="hasEnded">
            <v-list-item-content>
              <v-list-item-title>
                <h6 class="text-danger">
                  The schedule for this movie has ended!
                </h6>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-btn
            color="primary"
            :loading="loading"
            :disabled="hasEnded"
            min-height="50px"
            class="w-100 h-5 mr-2 d-lg-inline"
            @click="onCheckout"
          >
            Checkout
            <template v-slot:loader>
              <span class="custom-loader">
                <v-icon light>mdi-cached</v-icon>
              </span>
            </template>
          </v-btn>
        </v-card>
      </div>
      <div class="col-12 col-lg-3">
        <h1>Movie Details</h1>
        <v-card>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                >Movie: <b>{{ movie.title }}</b></v-list-item-title
              >
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                >Start Time:
                <b>{{
                  movieScheduleDateTime(movieTime.startTime)
                }}</b></v-list-item-title
              >
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                >End Time:
                <b>{{
                  movieScheduleDateTime(movieTime.endTime)
                }}</b></v-list-item-title
              >
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                >Hall:
                <b
                  >{{ hall.name }} ({{ hall.has3D ? "3D" : "2D" }})</b
                ></v-list-item-title
              >
            </v-list-item-content>
          </v-list-item>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cinemaId: null,
      movieId: null,
      hallId: null,
      movieTimeId: null,
      selectedSeats: [],
      totalPrice: 0.0,
    };
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
    this.movieId = this.$route.params.movieId;
    this.hallId = this.$route.params.hallId;
    this.movieTimeId = this.$route.params.movieTimeId;
    this.getHall();
  },
  computed: {
    hasEnded() {
      return (
        this.formatDateTime(this.movieTime.endTime) <
        this.formatDateTime(new Date())
      );
    },
    loading() {
      return this.$store.state.movies.loading;
    },
    tickets() {
      return this.$store.state.tickets.tickets;
    },
    hall() {
      return this.$store.state.halls.hall;
    },
    movieTime() {
      return this.$store.state.movieTimes.movieTime;
    },
    movie() {
      return this.$store.state.movies.movie;
    },
    cinema() {
      return this.$store.state.cinemas.cinema;
    },
    currentUser() {
      return this.$store.state.users.user;
    },
  },
  methods: {
    getHall() {
      const query = {
        cinemaId: this.cinemaId,
        movieId: this.movieId,
        hallId: this.hallId,
      };
      this.$store
        .dispatch("getHall", query)
        .then(() => {
          this.getTickets();
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching hall!"
          );
        });
    },
    getMovieTime() {
      const query = {
        cinemaId: this.cinemaId,
        movieId: this.movieId,
        movieTimeId: this.movieTimeId,
      };
      this.$store.dispatch("getMovieTime", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching movie time!"
        );
      });
    },
    isSeatSelected(seat) {
      if (this.selectedSeats.includes(seat)) {
        return true;
      } else {
        return false;
      }
    },
    selectSeat(seat) {
      if (this.isSeatSelected(seat)) {
        const index = this.selectedSeats.indexOf(seat);
        if (index > -1) {
          this.selectedSeats.splice(index, 1);
          this.totalPrice -= seat.ticket.price;
        }
      } else {
        this.selectedSeats.push(seat);
        this.totalPrice += seat.ticket.price;
      }
    },
    getTickets() {
      const query = {
        cinemaId: this.cinema.id,
        hallId: this.hallId,
        movieTimeId: this.movieTimeId,
      };
      this.$store
        .dispatch("getTickets", query)
        .then(() => {
          this.hall.rows.forEach((row) => {
            row.seats.forEach((seat) => {
              const seatWithTicket = seat;

              const ticket = {
                ticket: this.tickets.find((x) => x.seatId === seat.id),
              };

              Object.assign(seatWithTicket, ticket);
            });
          });
          this.getMovieTime();
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching tickets!"
          );
        });
    },
    getMovieTimes() {
      const query = {
        cinemaId: this.cinema.id,
        movieId: this.movie.id,
      };
      this.$store.dispatch("getMovieTimes", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching movie times!"
        );
      });
    },
    onCheckout() {
      if (this.selectedSeats.length < 1) {
        this.infoToast("Please select at least one seat!");
      } else {
        const ticketIds = this.selectedSeats.map((seat) => seat.ticket.id);

        const query = {
          cinemaId: this.cinemaId,
          hallId: this.hallId,
          movieTimeId: this.movieTimeId,
          model: {
            ticketsId: ticketIds,
            ownerId: this.currentUser.id,
          },
        };
        this.$store
          .dispatch("reserveTickets", query)
          .then((ok) => {
            if (ok) {
              this.successToast("Your tickets have been reserved!");
              this.onRefresh();
            }
          })
          .catch((error) => {
            this.errorToast(
              error.response?.data?.errors[0] ||
                "Something went wrong while reserving tickets!"
            );
          });
      }
    },
    onRefresh() {
      this.selectedSeats = [];
      this.totalPrice = 0.0;
      this.getHall();
    },
  },
};
</script>
<style lang="css"></style>
