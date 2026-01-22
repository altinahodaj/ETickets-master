<template>
  <div class="container flex-wrap">
    <h1 class="d-flex justify-content-center">Cinemas</h1>

    <div v-if="loading"><loading-page /></div>

    <div v-else class="d-flex justify-content-center flex-wrap">
      <div v-for="cinema in cinemas" :key="cinema.id" class="ml-5 mr-5">
        <v-card :loading="loading" class="mx-auto my-12" max-width="374">
          <v-img
            height="250"
            width="374"
            :src="(cinema.photos && cinema.photos.length > 0) ? cinema.photos[0].imgClientPath : 'http://127.0.0.1:8000/assets/app_files/Cinemas/default-image.jpg'"
            cover
          ></v-img>

          <v-card-title>{{ cinema.name }}</v-card-title>

          <v-card-text>
            <v-row align="center" class="mx-0">
              <v-rating
                :value="4.5"
                color="amber"
                dense
                half-increments
                readonly
                size="14"
              ></v-rating>

              <div class="grey--text ms-4">4.5 (413)</div>
            </v-row>

            <div class="my-4 text-subtitle-1">
              <v-icon light>place</v-icon>
              • {{ `${cinema.city}, ${cinema.address}` }}
            </div>
          </v-card-text>

          <v-divider class="mx-4"></v-divider>

          <v-card-title>Tonight's availability</v-card-title>

          <v-card-text>
            <v-chip-group active-class="deep-purple accent-4 white--text" column>
              <v-chip>5:30PM</v-chip>
              <v-chip>7:30PM</v-chip>
              <v-chip>8:00PM</v-chip>
              <v-chip>9:00PM</v-chip>
            </v-chip-group>
          </v-card-text>

          <v-card-actions class="d-flex justify-content-between">
            <v-btn
              outlined
              color="deep-purple lighten-2"
              text
              @click="onDetailsClick(cinema.id)"
            >
              See Details
            </v-btn>

            <v-btn
              outlined
              color="primary lighten-2"
              text
              @click="onMoviesClick(cinema.id)"
            >
              See Movies
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Cinemas",
  data() {
    return {
      search: "",
    };
  },
  created() {
    this.getCinemas();
  },
  computed: {
    loading() {
      return this.$store.state.cinemas.loading;
    },
    cinemas() {
      return this.$store.state.cinemas.cinemas;
    },
    filter() {
      return this.cinemas.filter((temp) => temp.name.match(this.search));
    },
  },
  methods: {
    // ✅ KJO E ZGJIDH FOTOJEN
    getCinemaImage(cinema) {
      const photos = cinema?.photos || [];
      if (photos.length > 0 && photos[0]?.imgClientPath) {
        return photos[0].imgClientPath;
      }

      // Default image (opsioni 1: përdor backend default)
      return "http://127.0.0.1:8000/assets/app_files/Cinemas/default-image.jpg";

      // (opsioni 2: nëse ke në frontend assets lokal, atëherë përdor require)
      // return require("@/assets/app_files/Cinemas/default-image.jpg");
    },

    onDetailsClick(cinemaId) {
      this.$router.push({
        name: "cinema-public-details",
        params: { cinemaId },
      });
    },
    onMoviesClick(cinemaId) {
      this.changeCinema(cinemaId);
      this.$router.push({
        name: "Movies",
        params: { cinemaId },
      });
    },
    changeCinema(cinemaId) {
      this.$store.dispatch("getCinema", cinemaId).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching cinema!"
        );
      });
    },
    getCinemas() {
      this.$store.dispatch("getCinemas").catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching cinemas!"
        );
      });
    },
  },
};
</script>

<style scoped>
.card {
  flex-direction: row;
  justify-content: center;
}
input {
  border: 1px solid black;
  padding: 20px;
  margin-top: 2%;
  margin-bottom: 2%;
  border-radius: 15px;
}
</style>
