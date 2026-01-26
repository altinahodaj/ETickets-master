<template>
  <div>
    <v-row v-if="loading" justify="center">
      <v-progress-circular indeterminate />
    </v-row>

    <v-row v-else-if="actorsToShow.length" dense>
      <v-col
        v-for="a in actorsToShow"
        :key="a.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card class="pa-3" elevation="2">
          <div class="d-flex align-center">
            <v-avatar size="56" class="mr-3">
              <v-img
                v-if="a.photos && a.photos.length"
                :src="a.photos[0].imgClientPath"
              />
              <v-img
                v-else
                src="http://127.0.0.1:8000/assets/app_files/Actors/default-image.jpg"
              />
            </v-avatar>

            <div>
              <div class="font-weight-bold">
                {{ a.firstName }} {{ a.lastName }}
              </div>
              <div class="grey--text text--darken-1 text-caption">
                {{ a.nationality || "" }}
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <div v-else class="text-center grey--text">
      No actors for this movie.
    </div>
  </div>
</template>

<script>
import api from "@/libs/api";

export default {
  name: "MovieActors",
  props: {
    cinemaId: { type: [Number, String], required: false, default: null },
    movieId: { type: [Number, String], required: false, default: null },
    actorsProp: { type: Array, required: false, default: () => [] },
  },
  data() {
    return {
      loading: false,
      actors: [],
      // track last fetched ids to avoid stale reuse
      lastFetched: { cinemaId: null, movieId: null },
    };
  },
  computed: {
    // Resolve cinemaId/movieId from props, parent (MovieDetails), route or store
    currentCinemaId() {
      const fromProp = this.cinemaId ?? null;
      const fromParent = this.$parent && this.$parent.cinemaId ? this.$parent.cinemaId : null;
      const fromRoute = this.$route && this.$route.params ? this.$route.params.cinemaId : null;
      const fromStore = this.$store && this.$store.state && this.$store.state.cinemas && this.$store.state.cinemas.cinema ? this.$store.state.cinemas.cinema.id : null;
      const v = fromProp ?? fromParent ?? fromRoute ?? fromStore ?? null;
      const n = Number(v);
      return Number.isFinite(n) && n > 0 ? n : null;
    },

    currentMovieId() {
      const fromProp = this.movieId ?? null;
      const fromParent = this.$parent && this.$parent.movieId ? this.$parent.movieId : null;
      const fromRoute = this.$route && this.$route.params ? this.$route.params.movieId : null;
      const fromStore = this.$store && this.$store.state && this.$store.state.movies && this.$store.state.movies.movie ? this.$store.state.movies.movie.id : null;
      const v = fromProp ?? fromParent ?? fromRoute ?? fromStore ?? null;
      const n = Number(v);
      return Number.isFinite(n) && n > 0 ? n : null;
    },
    actorsToShow() {
      // ✅ nëse MovieDetails i ka aktorët → përdori ata
      if (Array.isArray(this.actorsProp) && this.actorsProp.length) {
        return this.actorsProp;
      }
      // përndryshe përdor fetched actors
      return this.actors;
    },
  },
  watch: {
    // watch resolved ids (not raw props) so fetch runs when parent/route/store updates
    currentCinemaId: "fetchActorsIfNeeded",
    currentMovieId: "fetchActorsIfNeeded",
    actorsProp: "fetchActorsIfNeeded",
  },
  mounted() {
    this.fetchActorsIfNeeded();
  },
  methods: {
    fetchActorsIfNeeded() {
      // Nëse kemi actorsProp nga movie → mos bëj fetch
      if (Array.isArray(this.actorsProp) && this.actorsProp.length) return;

      const cinemaId = this.currentCinemaId;
      const movieId = this.currentMovieId;

      // require both ids to be present
      if (!cinemaId || !movieId) return;

      // If we've already fetched actors for the same movie+cinema, skip refetch
      if (
        this.lastFetched.cinemaId === cinemaId &&
        this.lastFetched.movieId === movieId &&
        this.actors && this.actors.length
      ) {
        return;
      }

      this.loading = true;

      // Always fetch actors fresh for the current movie (no global caching)
      api("movies")
        .get(`cinemas/${cinemaId}/movies/${movieId}/actors`)
        .then((res) => {
          this.actors = res.data.result || [];
          this.lastFetched = { cinemaId, movieId };
        })
        .catch(() => {
          this.actors = [];
          this.lastFetched = { cinemaId: null, movieId: null };
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>
