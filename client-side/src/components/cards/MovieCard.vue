<template>
  <div>
    <v-card :loading="loading" class="mx-auto my-12" max-width="374">
      <v-img
        height="300"
        aspect-ratio="2/3"
        :src="posterSrc"
        cover
      ></v-img>

      <v-card-title>{{ movie.title }}</v-card-title>

      <!-- Rating (REAL) -->
      <div
        v-if="!hideDetails"
        class="pa-2 d-flex justify-content-center align-center justify-content-between"
      >
        <v-rating
          :value="avgRating"
          color="amber"
          dense
          half-increments
          readonly
        ></v-rating>

        <span class="grey--text ms-4">
          {{ avgRating.toFixed(1) }} ({{ totalReviews }})
        </span>
      </div>

      <!-- Release year (vetëm nëse ekziston) -->
      <span v-if="!hideDetails && (movie.releaseYear || movie.release_year)" class="pa-1 d-flex align-center">
        <span class="ml-2 mr-2 align-center">Release Year:</span>
        {{ movie.releaseYear || movie.release_year }}
      </span>

      <!-- Country / Language (pa undefined) -->
      <div v-if="!hideDetails && countryLanguageText" class="ml-4 my-4 text-subtitle-1">
        <v-icon light>language</v-icon>
        • {{ countryLanguageText }}
      </div>

      <v-divider class="mx-4"></v-divider>

      <h6 class="ml-5">Genres</h6>
      <v-card-text>
        <v-chip-group active-class="deep-purple accent-4 white--text" column>
          <v-chip v-for="(g, i) in genres" :key="i">
            {{ g }}
          </v-chip>

          <div v-if="genres.length === 0" class="grey--text text--darken-1">
            No genres
          </div>
        </v-chip-group>
      </v-card-text>

      <v-card-actions class="d-flex justify-content-between">
        <v-btn
          outlined
          color="deep-purple lighten-2"
          text
          @click="onDetailsClick(movie.id)"
        >
          See Details
        </v-btn>

        <v-btn
          outlined
          color="primary lighten-2"
          text
          @click="onDetailsClick(movie.id)"
        >
          See Schedule
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    hideDetails: {
      default: false,
      required: false,
    },
    movie: {
      type: Object,
      required: true,
    },
  },

  computed: {
    loading() {
      return this.$store.state.movies.loading;
    },

    posterSrc() {
      const photos = this.movie?.photos || [];
      if (photos.length > 0) {
        const p = photos[0];
        return p.imgClientPath || p.img_client_path || "http://127.0.0.1:8000/assets/app_files/Movies/default-image.jpg";
      }
      return "http://127.0.0.1:8000/assets/app_files/Movies/default-image.jpg";
    },

    // ✅ backend po i kthen: avgRating/avg_rating, totalReviews/total_reviews
    avgRating() {
      const v = Number(this.movie?.avgRating ?? this.movie?.avg_rating ?? 0);
      return Number.isFinite(v) ? v : 0;
    },

    totalReviews() {
      const v = Number(this.movie?.totalReviews ?? this.movie?.total_reviews ?? 0);
      return Number.isFinite(v) ? v : 0;
    },

    countryLanguageText() {
      const country = this.movie?.country;
      const language = this.movie?.language;

      if (country && language) return `${country}/${language}`;
      if (country) return country;
      if (language) return language;
      return "";
    },

    // genre mund të vijë si string "Sci-Fi"
    // ose në të ardhmen si array ["Sci-Fi","Action"]
    genres() {
      const g = this.movie?.genre;

      if (!g) return [];

      if (Array.isArray(g)) return g.filter(Boolean);

      // nëse është string me presje "Sci-Fi, Action"
      if (typeof g === "string") {
        return g
          .split(",")
          .map((x) => x.trim())
          .filter(Boolean);
      }

      return [];
    },
  },

  methods: {
    onDetailsClick(movieId) {
      this.$router.push({
        name: "Movie",
        params: { movieId },
      });
    },
  },
};
</script>
