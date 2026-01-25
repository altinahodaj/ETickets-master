<template>
  <div class="ticket mt-15 mb-15">
    <div class="holes-top"></div>
    <div class="title">
      <p class="cinema">CINEMA VERSE PRESENTS</p>
      <img
        class="ml-8"
        src="/assets/app_files/main-logo_1.jpg"
        style="height: 50px"
        alt="Logo"
      />
    </div>
    <div class="poster">
      <img :src="posterSrc" :alt="posterAlt" @error="onPosterError" />
    </div>
    <div class="ticket-info">
      <table>
        <tr>
          <th>SCREEN</th>
          <th>ROW</th>
          <th>SEAT</th>
          <th>TYPE</th>
        </tr>
        <tr>
          <td class="bigger">{{ screenLabel }}</td>
          <td class="bigger">{{ rowLabel }}</td>
          <td class="bigger">{{ seatLabel }}</td>
          <td class="bigger">{{ is3D ? "3D" : "2D" }}</td>
        </tr>
      </table>
      <table>
        <tr>
          <th>PRICE</th>
          <th>TIME</th>
        </tr>
        <tr>
          <td class="bigger">{{ ticket.price }}€</td>
          <td class="bigger">
            {{ movieScheduleDateTime(movieStartTime) }}
          </td>
        </tr>
      </table>
    </div>
    <div class="holes-lower"></div>
    <div class="barcode">
      <barcode :value="shortBarcode"> Barcode Failed. </barcode>
    </div>
  </div>
</template>

<script>
import Barcode from "vue-barcode";

export default {
  components: { Barcode },
  data() {
    return {
      blackBarcode: "<td bgcolor='black'>",
      whiteBarcode: "<td bgcolor='white'>",
    };
  },
  computed: {
    moviesBaseUrl() {
      // FastAPI base (also where /assets is mounted)
      return process.env.VUE_APP_MOVIES_ENV || "http://127.0.0.1:8000";
    },
    movieTitle() {
      return this.ticket.movieTitle || this.ticket.movie_title || "";
    },
    titlePosterSrc() {
      const title = String(this.movieTitle || "").toLowerCase();
      if (!title) return "";

      // Local Vue public assets
      if (title.includes("interstellar")) return "/assets/app_files/Movies/interstellar-cover.jpg.jpg";
      if (title.includes("terminator")) return "/assets/app_files/Movies/terminator.jpg.jpg";
      if (title.includes("minions")) return "/assets/app_files/Movies/minions-rise-of-gru.jpg.jpg";
      if (title.includes("thor")) return "/assets/app_files/Movies/Thor-Love-and-Thunder-2.jpg.jpg";

      // Zootopia image currently exists under backend assets
      if (title.includes("zootopia")) {
        return `${this.moviesBaseUrl}/assets/app_files/Movies/zootopia_landscape.jpg`;
      }

      // The Housemaid images exist under backend assets
      if (title.includes("housemaid") || title.includes("house maid") || title.includes("the housemaid")) {
        return `${this.moviesBaseUrl}/assets/app_files/Movies/thehousemaid_landscape.jpg`;
      }

      return "";
    },
    posterSrc() {
      return (
        this.ticket.moviePosterUrl ||
        this.ticket.movie_poster_url ||
        this.ticket.moviePoster ||
        this.ticket.movie_poster ||
        this.ticket.imgClientPath ||
        this.ticket.img_client_path ||
        this.titlePosterSrc ||
        "/assets/app_files/Movies/default-image.jpg"
      );
    },
    posterAlt() {
      return this.movieTitle ? `Movie: ${this.movieTitle}` : "Movie poster";
    },
    shortBarcode() {
      const code = this.ticket.ticketCode || this.ticket.ticket_code || "";
      return code ? code.substring(0, 11) : "";
    },
    is3D() {
      return Boolean(
        this.ticket.is3D !== undefined ? this.ticket.is3D : this.ticket.is_3d
      );
    },
    movieStartTime() {
      return this.ticket.movieStartTime || this.ticket.movie_start_time || null;
    },
    screenLabel() {
      const hallNumber = this.ticket.hallNumber;
      const hallId = this.ticket.hallId !== undefined ? this.ticket.hallId : this.ticket.hall_id;
      return hallNumber !== null && hallNumber !== undefined ? hallNumber : (hallId || "-");
    },
    rowLabel() {
      return this.ticket.rowName || this.ticket.row_name || "-";
    },
    seatLabel() {
      return this.ticket.seatName || this.ticket.seat_name || "-";
    },
  },
  methods: {
    onPosterError(e) {
      if (e && e.target) {
        e.target.src = "/assets/app_files/Movies/default-image.jpg";
      }
    },
  },
  filters: {
    truncate: function (text, length, suffix) {
      if (text.length > length) {
        return text.substring(0, length) + suffix;
      } else {
        return text;
      }
    },
  },
  props: {
    ticket: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
// Variables
$card-color: linear-gradient(-45deg, #8067b7, #ec87c0);
$background-color: white;
$subtitle-color: rgb(231, 231, 231);
$width: 300;
$circle-size: 40;

body {
  font-family: "Yanone Kaffeesatz", sans-serif;
  font-weight: 600;
}

img {
  max-width: 100%;
  height: 250px;
}

.ticket {
  width: 300px;
  height: 775px;
  background-image: $card-color;
  margin: 25px auto;
  position: relative;
}

.holes-top {
  height: $circle-size + px;
  width: $circle-size + px;
  background-color: $background-color;
  border-radius: 50%;
  position: absolute;
  left: 50%;
  margin-left: ($circle-size / -2) + px;
  top: ($circle-size / -2) + px;

  &:before,
  &:after {
    content: "";
    height: $circle-size + px;
    width: $circle-size + px;
    background-color: $background-color;
    position: absolute;
    border-radius: 50%;
  }
  &:before {
    left: ($width / -2) + px;
  }
  &:after {
    left: ($width / 2) + px;
  }
}

.holes-lower {
  position: relative;
  margin: 25px;
  border: 1px dashed #aaa;
  &:before,
  &:after {
    content: "";
    height: $circle-size + px;
    width: $circle-size + px;
    background-color: $background-color;
    position: absolute;
    border-radius: 50%;
  }

  &:before {
    top: -25px;
    left: ($circle-size / -1) + px;
  }
  &:after {
    top: -25px;
    left: ($width - $circle-size) + px;
  }
}

.title {
  padding: 50px 25px 10px;
}

.cinema {
  color: $subtitle-color;
  font-size: 18px;
}

.movie-title {
  font-size: 35px;
  color: white;
}
.ticket-info {
  padding: 15px 25px;
}
table {
  width: 100%;
  font-size: 18px;
  margin-bottom: 15px;
  color: white;
  tr {
    margin-bottom: 10px;
  }
  th {
    color: $subtitle-color;
    text-align: left;
    &:nth-of-type(1) {
      width: 38%;
    }
    &:nth-of-type(2) {
      width: 40%;
    }
    &:nth-of-type(3) {
      width: 15%;
    }
  }

  td {
    width: 33%;
    font-size: 32px;
  }
}
.bigger {
  font-size: 20px;
  font-weight: 400;
}
.barcode {
  background-image: $card-color;
  div::v-deep {
    max-width: 100px;
    .vue-barcode-element > rect {
      fill: #8067b7 !important;
    }
  }
}
</style>
