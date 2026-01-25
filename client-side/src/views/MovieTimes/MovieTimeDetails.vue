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
          <v-alert
            v-if="!((hall.rows || []).length)"
            type="info"
            border="left"
            class="mx-auto"
            style="max-width: 720px"
          >
            No seats are configured for this hall yet. Ask an admin to generate rows/seats for this hall, then reload this page.
          </v-alert>
          <div
            v-for="row in (hall.rows || [])"
            :key="row.id"
            class="d-flex justify-content-center w-100"
          >
            <div
              v-for="seat in (row.seats || [])"
              :key="seat.id"
              :class="row.isVipRow ? 'm-3' : 'm-1'"
            >
              <v-btn
                v-if="seat.isVipSeat"
                :disabled="!seat.ticket || !((seat.ticket.isAvailable !== undefined ? seat.ticket.isAvailable : seat.ticket.is_available)) || hasEnded"
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
                :disabled="!seat.ticket || !((seat.ticket.isAvailable !== undefined ? seat.ticket.isAvailable : seat.ticket.is_available)) || hasEnded"
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
      <div class="col-12 col-lg-3" v-if="movieTime && movieTime.id">
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

    console.log("--- MovieTimeDetails Created ---");
    console.log("Cinema ID:", this.cinemaId);
    console.log("Movie ID:", this.movieId);
    console.log("Hall ID:", this.hallId);
    console.log("MovieTime ID:", this.movieTimeId);
    console.log("--------------------------------");

    if (!this.cinemaId || this.cinemaId === "undefined" || this.cinemaId === "0") {
        this.errorToast("Invalid Cinema ID. Redirecting...");
        setTimeout(() => this.$router.push({ name: "Home" }), 2000);
        return;
    }

    this.getHall();
    this.getMovie();
    this.getCinema();
  },
  computed: {
    hasEnded() {
      if (!this.movieTime || !this.movieTime.endTime) return false;
      const endTimeStr = this.movieTime.endTime;
      // Use smarter parsing: if it has timezone info (+ or Z), use it. 
      // Otherwise, assume local time if it's returning from a local server.
      // But FastAPI/Pydantic dates are usually UTC-ish if not specified.
      // Let's try parsing it directly first.
      const end = new Date(endTimeStr);
      // If direct parsing results in an invalid date or we want to be safe about UTC:
      if (isNaN(end.getTime())) {
          return false;
      }
      return end < new Date();
    },
    loading() {
      // Tani çdo modul ka loading-un e vet.
      return this.$store.state.halls.loading || this.$store.state.tickets.loading || this.$store.state.movieTimes.loading;
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
            error.response?.data?.errors?.[0] ||
            error.response?.data?.detail?.[0]?.msg ||
              "Something went wrong while fetching hall!"
          );
        });
    },
    getMovie() {
      const query = {
        cinemaId: this.cinemaId,
        movieId: this.movieId,
      };
      this.$store.dispatch("getMovie", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors?.[0] ||
          error.response?.data?.detail?.[0]?.msg ||
            "Something went wrong while fetching movie!"
        );
      });
    },
    getCinema() {
      this.$store.dispatch("getCinema", this.cinemaId).catch((error) => {
        this.errorToast(
          error.response?.data?.errors?.[0] ||
          error.response?.data?.detail?.[0]?.msg ||
            "Something went wrong while fetching cinema!"
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
          error.response?.data?.errors?.[0] ||
          error.response?.data?.detail?.[0]?.msg ||
            "Something went wrong while fetching movie time!"
        );
      });
    },
    isSeatSelected(seat) {
      if (!seat) return false;
      return (this.selectedSeats || []).some((s) => String(s?.id) === String(seat.id));
    },
    selectSeat(seat) {
      if (!seat || !seat.ticket) return;

      const price = Number(seat.ticket.price ?? 0);
      const idx = (this.selectedSeats || []).findIndex(
        (s) => String(s?.id) === String(seat.id)
      );

      if (idx > -1) {
        this.selectedSeats.splice(idx, 1);
        this.totalPrice -= price;
        return;
      }

      // ensure no duplicates by seat id
      this.selectedSeats.push(seat);
      this.totalPrice += price;
    },
    getTickets() {
      const query = {
        cinemaId: this.cinemaId,
        hallId: this.hallId,
        movieTimeId: this.movieTimeId,
      };
      this.$store
        .dispatch("getTickets", query)
        .then(() => {
          // Nese s'ka tickets ende per kete orar, i gjenerojme automatikisht.
          if (!this.tickets || this.tickets.length === 0) {
            return this.$store
              .dispatch("generateTickets", query)
              .then(() => this.$store.dispatch("getTickets", query))
              .then(() => {
                this.attachTicketsToSeats();
                this.getMovieTime();
              });
          }

          this.attachTicketsToSeats();
          this.getMovieTime();
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors?.[0] ||
            error.response?.data?.detail?.[0]?.msg ||
              "Something went wrong while fetching tickets!"
          );
        });
    },
    attachTicketsToSeats() {
      const ticketBySeatId = new Map(
        (this.tickets || []).map((t) => [t.seatId ?? t.seat_id, t])
      );

      (this.hall.rows || []).forEach((row) => {
        (row.seats || []).forEach((seat) => {
          const rawTicket = ticketBySeatId.get(seat.id);
          if (!rawTicket) {
            seat.ticket = null;
            return;
          }

          seat.ticket = {
            ...rawTicket,
            seatId: rawTicket.seatId ?? rawTicket.seat_id,
            isAvailable: rawTicket.isAvailable ?? rawTicket.is_available,
          };
        });
      });
    },
    getMovieTimes() {
      const query = {
        cinemaId: this.cinemaId,
        movieId: this.movieId,
      };
      this.$store.dispatch("getMovieTimes", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors?.[0] ||
          error.response?.data?.detail?.[0]?.msg ||
            "Something went wrong while fetching movie times!"
        );
      });
    },
    onCheckout() {
      if (this.selectedSeats.length < 1) {
        this.infoToast("Please select at least one seat!");
      } else {
        if (!this.currentUser || !this.currentUser.id) {
          this.infoToast("Please login to reserve tickets.");
          this.$router.push({ name: "Login" });
          return;
        }
        const ticketIds = Array.from(
          new Set(
            (this.selectedSeats || [])
              .map((seat) => seat?.ticket?.id)
              .filter((id) => id !== null && id !== undefined)
              .map((id) => String(id))
          )
        ).map((id) => Number(id));

        if (!ticketIds.length) {
          this.errorToast("No valid tickets selected.");
          return;
        }

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
              this.$router.push({ name: "MyTickets" });
            }
          })
          .catch((error) => {
            this.errorToast(
              error.response?.data?.errors?.[0] ||
              error.response?.data?.detail?.[0]?.msg ||
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
