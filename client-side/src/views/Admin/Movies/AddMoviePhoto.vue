<template>
  <div>
    <v-row>
      <v-col cols="9">
        <h2>Add Movie Photos</h2>
      </v-col>
      <v-col class="d-flex align-content-end" cols="3">
        <v-btn
          color="blue-grey"
          class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
          @click="goBack(cinemaId, movieId)"
        >
          <v-icon dark left> mdi-arrow-left </v-icon>Back
        </v-btn>
      </v-col>
    </v-row>
    <hr />
    <div class="container mt-5">
      <v-col class="d-flex align-center justify-content-center" cols="12">
        <div class="d-flex flex-column mb-5 w-50">
          <h2 class="d-flex justify-content-center mb-5">Add photos below!</h2>
          <v-file-input
            v-model="files"
            counter
            type="file"
            label="File input"
            multiple
            placeholder="Select your files"
            prepend-icon="mdi-paperclip"
            outlined
            :show-size="1000"
          >
            <template v-slot:selection="{ index, text }">
              <v-chip v-if="index < 2" color="primary" dark label small>
                {{ text }}
              </v-chip>

              <span
                v-else-if="index === 2"
                class="text-overline grey--text text--darken-3 mx-2"
              >
                +{{ files.length - 2 }} File(s)
              </span>
            </template>
          </v-file-input>
          <v-btn
            :loading="loading"
            :disabled="loading"
            color="success"
            class="mr-2"
            @click="addMovieImages()"
          >
            <v-icon left dark> mdi-camera </v-icon>
            Add Image{{ files.length > 1 ? "s" : "" }}
          </v-btn>
        </div>
      </v-col>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      files: [],
      cinemaId: null,
      movieId: null,
    };
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
    this.movieId = this.$route.params.movieId;
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
    addMovieImages() {
      const formData = new FormData();
      this.files.forEach((file) => {
        formData.append(`files`, file);
      });
      this.$store
        .dispatch("addMoviePhotos", {
          cinemaId: this.cinemaId,
          movieId: this.movieId,
          files: formData,
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while adding photos!"
          );
        });
      this.goBack(this.cinemaId, this.movieId);
    },
    goBack(cinemaId, movieId) {
      this.$router.push({
        name: "movie-details",
        params: { cinemaId: cinemaId, movieId: movieId },
      });
    },
  },
};
</script>
