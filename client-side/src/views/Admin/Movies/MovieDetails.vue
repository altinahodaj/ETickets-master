<template>
  <div>
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <v-row>
        <v-col cols="9">
          <h2>Movie Details</h2>
        </v-col>
        <v-col class="d-flex align-content-end" cols="3">
          <v-btn
            class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
            color="success"
            @click="redirectToAddPhoto(cinemaId, movieId)"
          >
            <v-icon left dark> mdi-camera </v-icon>
            Add Images
          </v-btn>
          <v-btn
            class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
            color="primary"
            @click="redirectToMovieTimes(cinemaId, movieId)"
          >
            <v-icon left dark> schedule </v-icon>
            View Schedule
          </v-btn>
        </v-col>
      </v-row>

      <hr />
      <div class="container mt-5">
        <v-col class="d-flex align-center justify-content-center" cols="12">
          <v-item v-if="movie.photos.length > 0">
            <v-carousel>
              <v-carousel-item
                v-for="(photo, i) in movie.photos"
                :key="i"
                :src="photo.imgClientPath"
                reverse-transition="fade-transition"
                transition="fade-transition"
              >
                <div class="d-flex align-content-end p-3">
                  <v-btn
                    class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
                    color="error"
                    @click="removePhoto(cinemaId, movieId, photo)"
                  >
                    <v-icon left dark> mdi-close </v-icon>
                    Remove
                  </v-btn>
                </div>
              </v-carousel-item>
            </v-carousel>
          </v-item>
          <div v-else class="d-flex flex-column mb-5">
            <h2>There are no photos for this movie!</h2>
            <v-btn
              color="success"
              class="mr-2"
              @click="redirectToAddPhoto(cinemaId, movieId)"
            >
              <v-icon left dark> mdi-camera </v-icon>
              Add Image
            </v-btn>
          </div>
        </v-col>

        <v-item-group active-class="primary">
          <v-container>
            <v-row>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Title:
                    <h6>{{ movie.title }}</h6>
                  </span>
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <div>
                    <span>Actors:</span>
                    <div v-if="movie.actors.length > 0">
                      <b-avatar-group size="60px" class="actors-container">
                        <div
                          class="d-flex justify-content-center w-100"
                          @click="onActorDetailsClick(actor.id)"
                          v-b-tooltip.hover
                          :title="`${actor.firstName} ${actor.lastName}`"
                          v-for="actor in movie.actors"
                          :key="actor.id"
                        >
                          <b-avatar
                            :src="actor.photos[0].imgClientPath"
                            variant="dark"
                          >
                          </b-avatar>
                        </div>
                      </b-avatar-group>
                    </div>
                  </div>
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Description:
                    <h6>{{ movie.description }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Trailer Link:
                    <h6>{{ movie.trailerLink }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Release Year:
                    <h6>{{ movie.releaseYear }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Release Date:
                    <h6>{{ movie.releaseDate }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Country:
                    <h6>{{ movie.country }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Language:
                    <h6>{{ movie.language }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Genre:
                    <h6>{{ movie.genre }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Movie Length (minutes):
                    <h6>{{ movie.length }}</h6></span
                  >
                </v-item>
              </v-col>
            </v-row>
          </v-container>
        </v-item-group>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, numberInt, minValueRule } from "@/helpers/validations";
import { setInteractionMode } from "vee-validate";

setInteractionMode("eager");

export default {
  components: {},
  data() {
    return {
      cinemaId: null,
      movieId: null,
      required,
      numberInt,
      minValueRule,
    };
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
    this.movieId = this.$route.params.movieId;
    const query = {
      cinemaId: this.cinemaId,
      movieId: this.movieId,
    };
    this.getMovie(query);
  },
  computed: {
    loading() {
      return this.$store.state.movies.loading;
    },
    movie() {
      return this.$store.state.movies.movie;
    },
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    removePhoto(cinemaId, movieId, photo) {
      this.$store
        .dispatch("removeMoviePhoto", {
          cinemaId: cinemaId,
          movieId: movieId,
          photoId: photo.longId,
        })
        .then(() => {
          this.getMovie({ cinemaId: cinemaId, movieId: movieId });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while deleting photo!"
          );
        });
    },
    getMovie(query) {
      this.$store.dispatch("getMovie", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching movie!"
        );
      });
    },
    onActorDetailsClick(actorId) {
      this.$router.push({
        name: "actor-details",
        params: { actorId },
      });
    },
    redirectToAddPhoto(cinemaId, movieId) {
      this.$router.push({
        name: "movie-add-photo",
        params: { cinemaId: cinemaId, movieId: movieId },
      });
    },
    redirectToMovieTimes(cinemaId, movieId) {
      this.$router.push({
        name: "movie-times",
        params: { cinemaId: cinemaId, movieId: movieId },
      });
    },
  },
};
</script>
<style lang="css">
.actors-container > div {
  flex-wrap: nowrap !important;
}
</style>
