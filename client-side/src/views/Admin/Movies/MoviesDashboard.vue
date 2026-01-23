<template>
  <div class="table-wrapper p-2 movies">
    <v-row>
      <v-col cols="9">
        <h2>Movies</h2>
      </v-col>
      <v-col cols="3">
        <v-select
          solo
          v-model="selectedCinema"
          :items="getObjectOptionsName(cinemas)"
          @change="changeCinema()"
          label="Select Movie"
        ></v-select>
      </v-col>
    </v-row>

    <hr />
    <div class="d-flex mb-5 movies-header">
      <div>
        <v-btn color="success" class="mr-2" @click="onCreateMovie()">
          <v-icon left dark> mdi-plus </v-icon>
          Create Movie
        </v-btn>
      </div>
      <div>
        <v-btn
          color="primary"
          :disabled="!isSelected"
          class="mr-2 d-lg-inline action-movie-button"
          @click="onEditClick(selected[0].id)"
        >
          Edit
        </v-btn>
        <v-btn
          color="error"
          :loading="removingMovie"
          :disabled="!isSelected || removingMovie"
          class="mr-2 d-lg-inline action-movie-button"
          @click="onDeleteClick(selected[0].id)"
        >
          Delete
          <template v-slot:loader>
            <span class="custom-loader">
              <v-icon light>mdi-cached</v-icon>
            </span>
          </template>
        </v-btn>
      </div>
      <v-btn
        :loading="loading"
        :disabled="loading"
        color="blue-grey"
        class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
        @click="onRefresh()"
      >
        Refresh
        <v-icon right dark> mdi-refresh </v-icon>
        <template v-slot:loader>
          <span class="custom-loader">
            <v-icon light>mdi-cached</v-icon>
          </span>
        </template>
      </v-btn>
    </div>
    <!-- DESKTOP -->
    <div class="default-table position-relative d-lg-block">
      <v-data-table
        v-model="selected"
        :single-select="true"
        show-select
        :headers="headers"
        :items="movies"
        item-key="id"
        :items-per-page="10"
        :loading="loading"
        loading-text="Loading Movies... Please wait"
        :class="{ loaded: !loading }"
        class="elevation-1"
      >
        <template v-slot:[`item.title`]="{ item }">
          <a class="link" @click="onDetailsClick(item.id)">{{ item.title }}</a>
        </template>
        <template v-slot:[`item.image`]="{ item }">
          <v-avatar contain class="ma-2" color="blue">
            <img
              class="avatar-image"
              v-if="item.photos.length > 0"
              :src="item.photos[0].imgClientPath"
              :alt="item.id"
            />
            <img
              v-else
              src="/assets/app_files/Movies/default-image.jpg"
              class="avatar-image"
              :alt="item.id"
            />
          </v-avatar>
        </template>
        <template v-slot:[`item.actors`]="{ item }">
          <div v-if="item.actors.length > 0">
            <b-avatar-group size="45px">
              <b-avatar
                v-b-tooltip.hover
                :title="`${actor.firstName} ${actor.lastName}`"
                v-for="actor in item.actors"
                :key="actor.id"
                :src="actor.photos[0].imgClientPath"
                variant="dark"
              >
              </b-avatar>
            </b-avatar-group>
          </div>
        </template>
        <template v-slot:[`item.genre`]="{ item }">
          <v-chip class="ma-2" color="primary lighten-2">
            {{ item.genre }}
          </v-chip>
        </template>
        <template slot="no-data">
          <div v-if="loading" class="loading-table text-center py-1">
            <b-spinner variant="primary" />
          </div>
          <template v-else>
            <no-data
              no-data-text="No Movies have been added to this cinema yet..."
              create-text="+ Create Movie"
              access-page="Movies"
              @action="onCreateMovie()"
            />
          </template>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "Movies",
  components: {},
  data() {
    return {
      selected: [],
      headers: [
        {
          text: "Id",
          align: "start",
          sortable: false,
          value: "id",
        },
        { text: "Title", value: "title" },
        { text: "Image", value: "image" },
        { text: "Actors", value: "actors" },
        { text: "Trailer Link", sortable: false, value: "trailerLink" },
        { text: "Country", value: "country" },
        { text: "Language", value: "language" },
        { text: "Genre", value: "genre" },
      ],
      selectedCinema: null,
      fields: [
        {
          key: "selected",
          label: "",
          variant: "select",
          hide: true,
        },
        { key: "id" },
        { key: "title" },
        { key: "trailerLink" },
        { key: "country" },
        { key: "language" },
        { key: "genre" },
      ],
    };
  },
  computed: {
    loading() {
      return this.$store.state.movies.loading;
    },
    movies() {
      return this.$store.state.movies.movies;
    },
    cinemas() {
      return this.$store.state.cinemas.cinemas;
    },
    removingMovie() {
      return this.$store.state.movies.removingMovie;
    },
    isSelected() {
      return this.selected[0];
    },
  },
  created() {
    this.getCinemas();
  },
  methods: {
    onRefresh() {
      this.getMovies(this.selectedCinema);
    },
    getCinema() {
      this.$store.dispatch("getCinema").catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching cinemas!"
        );
      });
    },
    getCinemas() {
      this.$store
        .dispatch("getCinemas")
        .then(() => {
          if (this.selectedCinema == null) {
            this.selectedCinema = this.cinemas[0];
          }
          this.getMovies(this.selectedCinema);
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching cinemas!"
          );
        });
    },
    getMovies(selectedCinema) {
      this.$store.dispatch("getMovies", selectedCinema.id).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching movies!"
        );
      });
    },
    changeCinema() {
      if (this.selectedCinema != null) {
        this.getMovies(this.selectedCinema);
      }
    },
    onEditClick(movieId) {
      this.$router.push({
        name: "movie-edit",
        params: { cinemaId: this.selectedCinema.id, movieId: movieId },
      });
    },
    onDetailsClick(movieId) {
      this.$router.push({
        name: "movie-details",
        params: { cinemaId: this.selectedCinema.id, movieId: movieId },
      });
    },
    onCreateMovie() {
      this.$router.push({
        name: "movie-create",
        params: { cinemaId: this.selectedCinema.id },
      });
    },
    onDeleteClick(movieId) {
      this.confirmDelete(
        "Delete Movie",
        "Are you sure you want to delete this movie?"
      ).then((ok) => {
        if (ok) {
          this.$store
            .dispatch("removeMovie", {
              cinemaId: this.selectedCinema.id,
              movieId: movieId,
            })
            .then(() => {
              this.successToast("Movie was removed");
              this.selected = [];
              this.getMovies(this.selectedCinema);
            })
            .catch((error) => {
              this.errorToast(error.response.data.errors[0]);
            });
        }
      });
    },
  },
};
</script>
<style lang="scss">
.avatar-image {
  object-fit: cover;
}
</style>
