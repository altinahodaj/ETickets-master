<template>
  <div>
    <div v-if="loading"><loading-page /></div>

    <div v-else>
      <v-container class="mt-5">
        <v-row justify="center">
          <v-col cols="12" md="10" lg="9">
            <!-- PHOTO BANNER -->
            <div v-if="bannerList.length">
              <v-carousel
                height="360"
                hide-delimiters
                show-arrows-on-hover
                class="movie-carousel"
              >
                <v-carousel-item v-for="(photo, i) in bannerList" :key="i">
                  <v-img
                    :src="photo.img_client_path"
                    height="360"
                    cover
                    class="movie-banner"
                    gradient="to bottom, rgba(0,0,0,.10), rgba(0,0,0,.70)"
                  />
                </v-carousel-item>
              </v-carousel>
            </div>

            <div v-else class="d-flex flex-column mb-5 align-center">
              <h2>There are no photos for this movie!</h2>
            </div>

            <!-- MOVIE INFO CARD -->
            <v-card class="movie-info-card" elevation="2">
              <v-card-text>
                <div class="movie-title">{{ movieTitleText }}</div>

                <div class="movie-desc">
                  {{ movieDescriptionText | truncate(600, "...") }}
                </div>

                <v-row class="mt-2">
                  <!-- Release Year -->
                  <v-col cols="12" sm="4" v-if="releaseYearText">
                    <div class="meta">
                      <div class="meta-label">Release Year</div>
                      <div class="meta-value">{{ releaseYearText }}</div>
                    </div>
                  </v-col>

                  <!-- Length -->
                  <v-col cols="12" sm="4">
                    <div class="meta">
                      <div class="meta-label">Length</div>
                      <div class="meta-value">{{ lengthText }}</div>
                    </div>
                  </v-col>

                  <!-- Director -->
                  <v-col cols="12" sm="4">
                    <div class="meta">
                      <div class="meta-label">Director</div>
                      <div class="meta-value">{{ directorText }}</div>
                    </div>
                  </v-col>

                  <!-- Avg Rating (REAL from backend) -->
                  <v-col cols="12">
                    <div class="rating-row" v-if="hasRating">
                      <v-rating
                        :value="avgRatingNumber"
                        color="amber"
                        dense
                        half-increments
                        readonly
                      />
                      <span class="grey--text ms-4">
                        {{ avgRatingNumber.toFixed(1) }} ({{ totalReviewsNumber }})
                      </span>
                    </div>
                  </v-col>

                  <!-- Country / Language (NO undefined) -->
                  <v-col cols="12" v-if="countryLanguageText">
                    <div class="lang-row">
                      <v-icon small>language</v-icon>
                      <span class="ml-2">{{ countryLanguageText }}</span>
                    </div>
                  </v-col>

                  <!-- Genres -->
                  <v-col cols="12" v-if="genresText">
                    <div class="meta">
                      <div class="meta-label">Genres</div>
                      <div class="meta-value">{{ genresText }}</div>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <hr class="mt-6" />
          </v-col>
        </v-row>
      </v-container>

      <!-- TODAY SCHEDULE -->
      <div class="d-flex justify-content-center mb-10">
        <div class="container m0">
          <h1 class="d-flex justify-content-center mb-5">Today's Schedule</h1>
          <movie-schedules />
        </div>
      </div>

      <hr />

      <!-- CAST -->
      <div class="d-flex justify-content-center mb-10">
        <div class="container m0">
          <h1 class="d-flex justify-content-center mb-5">Cast</h1>
          <movie-actors />
        </div>
      </div>

      <hr />

      <!-- REVIEWS -->
      <div class="d-flex justify-content-center">
        <div class="container m0">
          <h1 class="d-flex justify-content-center mb-5">
            Reviews for this movie
          </h1>

          <div style="margin-top: 60px; margin-bottom: 60px">
            <v-card-text>
              <div class="font-weight-bold ml-8 mb-2">Reviews</div>

              <v-timeline align-top dense>
                <v-timeline-item v-for="review in reviews" :key="review.id" small>
                  <v-card class="pa-4 review-card">
                    <div class="font-weight-normal">
                      <h2 class="review-title">{{ review.reviewTitle }}</h2>
                    </div>

                    <v-rating
                      :value="Number(review.reviewRating || 0)"
                      name="reviewRating"
                      style="margin-top: 10px; margin-bottom: 20px"
                      color="amber"
                      dense
                      readonly
                    />

                    <div class="mb-3">{{ review.reviewDescription }}</div>

                    <div class="review-meta">
                      <strong>{{ review.userName }}</strong>
                      <span class="dot">•</span>
                      <span>@{{ movieScheduleDateTime(review.insertDate) }}</span>
                    </div>
                  </v-card>
                </v-timeline-item>
              </v-timeline>
            </v-card-text>
          </div>

          <hr />

          <h1 class="mt-3 d-flex justify-content-center">Post a Review</h1>
          <add-review />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, numberInt, minValueRule } from "@/helpers/validations";
import { setInteractionMode } from "vee-validate";
import MovieSchedules from "./MovieSchedules.vue";
import AddReview from "../../components/Reviews/AddReview.vue";
import MovieActors from "./MovieActors.vue";

setInteractionMode("eager");

export default {
  name: "MovieDetails",
  components: {
    MovieSchedules,
    AddReview,
    MovieActors,
  },
  data() {
    return {
      cinemaId: null,
      required,
      numberInt,
      minValueRule,
      todayDate: this.formatShortDateTime(new Date()),
      model: null,
      movieId: null,
    };
  },
  created() {
    this.movieId = Number(this.$route.params.movieId);

    // nëse cinema nuk është loaded, mos e rrëzo
    this.cinemaId = this.cinema?.id ?? null;

    this.getMovie(this.movieId);
    this.getReviews(this.movieId);
  },
  filters: {
    truncate(text, length, suffix) {
      if (!text) return "";
      return text.length > length ? text.substring(0, length) + suffix : text;
    },
  },
  computed: {
    loading() {
      return this.$store.state.movies.loading;
    },
    movie() {
      return this.$store.state.movies.movie || {};
    },
    cinema() {
      return this.$store.state.cinemas.cinema;
    },
    reviews() {
      return this.$store.state.reviews.reviews || [];
    },

    // ---------------------------
    // Banner selection (MovieDetails only)
    // ---------------------------
    bannerList() {
      const photos = Array.isArray(this.movie?.photos) ? this.movie.photos : [];

      // Nëse ke shtuar në DB photo_type="banner", filtroji këtu:
      const banners = photos.filter((p) => (p.photo_type || "").toLowerCase() === "banner");
      if (banners.length) return banners;

      // fallback: përdor foton e parë që ekziston
      return photos.length ? [photos[0]] : [];
    },

    // ---------------------------
    // Safe text fields
    // ---------------------------
    movieTitleText() {
      return this.movie?.title || "—";
    },
    movieDescriptionText() {
      return this.movie?.description || "";
    },

    releaseYearText() {
      // backend: release_year
      const v = this.movie?.release_year ?? this.movie?.releaseYear;
      return v ? String(v) : "";
    },

    lengthText() {
      // backend: length_minutes
      const m =
        this.movie?.length_minutes ??
        this.movie?.lengthMinutes ??
        this.movie?.length;

      const n = Number(m);
      if (!Number.isFinite(n) || n <= 0) return "—";
      return `${n} min`;
    },

    directorText() {
      return this.movie?.director ? this.movie.director : "—";
    },

    countryLanguageText() {
      const country = this.movie?.country;
      const language = this.movie?.language;

      if (country && language) return `${country}/${language}`;
      if (country) return country;
      if (language) return language;
      return "";
    },

    genresText() {
      // backend aktual: genre (string). Nëse më vonë e bën listë, e mbulon edhe atë.
      const g = this.movie?.genre;
      if (Array.isArray(g)) return g.filter(Boolean).join(", ");
      return g ? String(g) : "";
    },

    // ---------------------------
    // REAL rating from backend
    // ---------------------------
    avgRatingNumber() {
      const n = Number(this.movie?.avg_rating ?? this.movie?.avgRating ?? 0);
      return Number.isFinite(n) ? n : 0;
    },
    totalReviewsNumber() {
      const n = Number(this.movie?.total_reviews ?? this.movie?.totalReviews ?? 0);
      return Number.isFinite(n) ? n : 0;
    },
    hasRating() {
      return this.totalReviewsNumber > 0;
    },
  },
  methods: {
    getMovie(movieId) {
      const query = {
        cinemaId: this.cinemaId,
        movieId,
      };

      this.$store
        .dispatch("getMovie", query)
        .then(() => {
          this.getMovieTimes();
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors?.[0] ||
              "Something went wrong while fetching movie details!"
          );
        });
    },

    getReviews(movieId) {
      const query = { movieId };

      this.$store.dispatch("getReviews", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors?.[0] ||
            "Something went wrong while fetching reviews!"
        );
      });
    },

    getMovieTimes() {
      const query = {
        cinemaId: this.cinema?.id,
        movieId: this.movie?.id,
      };

      this.$store.dispatch("getMovieTimes", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors?.[0] ||
            "Something went wrong while fetching movie times!"
        );
      });
    },
  },
};
</script>

<style scoped>
.movie-carousel {
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
}

.movie-banner {
  border-radius: 14px;
}

.movie-info-card {
  margin-top: 16px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(6px);
}

.movie-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 10px;
}

.movie-desc {
  opacity: 0.9;
  line-height: 1.6;
  margin-bottom: 8px;
}

.meta-label {
  font-size: 12px;
  opacity: 0.7;
  margin-bottom: 4px;
}

.meta-value {
  font-size: 16px;
  font-weight: 600;
}

.lang-row {
  display: flex;
  align-items: center;
  opacity: 0.85;
  margin-top: 6px;
}

.rating-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 6px;
}

.review-card {
  border-radius: 12px;
}

.review-title {
  margin: 0;
}

.review-meta {
  opacity: 0.85;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  opacity: 0.6;
}
</style>
