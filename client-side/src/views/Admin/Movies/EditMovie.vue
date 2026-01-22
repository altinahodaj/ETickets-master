<template>
  <div>
    <h2>Edit Movie</h2>
    <hr />
    <div class="container mt-5">
      <validation-observer ref="observer" v-slot="{ invalid }">
        <form @submit.prevent="submit">
          <validation-provider
            v-slot="{ errors }"
            name="Title"
            rules="required|min:3"
          >
            <v-text-field
              v-model="movie.title"
              :error-messages="errors"
              label="Title"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Description"
            rules="required"
          >
            <v-textarea
              v-model="movie.description"
              :error-messages="errors"
              label="Description"
              outlined
              required
            ></v-textarea>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Actors"
            rules="required"
          >
            <v-select
              v-model="selectedActors"
              :error-messages="errors"
              outlined
              :items="getActorNames(allActors)"
              label="Select movie actors"
              multiple
              chips
            ></v-select>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Director"
            rules="required"
          >
            <v-text-field
              v-model="movie.director"
              :error-messages="errors"
              label="Director"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Trailer Link"
            rules="required"
          >
            <v-text-field
              v-model="movie.trailerLink"
              :error-messages="errors"
              label="Trailer Link"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Release Year"
            rules="required"
          >
            <v-text-field
              v-model.number="movie.releaseYear"
              type="number"
              :error-messages="errors"
              label="Release Year"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Release Date"
            rules="required"
          >
            <v-text-field
              v-model="movie.releaseDate"
              type="datetime-local"
              :error-messages="errors"
              label="Release Date"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Country"
            rules="required"
          >
            <v-text-field
              v-model="movie.country"
              :error-messages="errors"
              label="Country"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Language"
            rules="required"
          >
            <v-text-field
              v-model="movie.language"
              :error-messages="errors"
              label="Language"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Genre"
            rules="required"
          >
            <v-text-field
              v-model="movie.genre"
              :error-messages="errors"
              label="Genre"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Length"
            rules="required"
          >
            <v-text-field
              v-model.number="movie.length"
              type="number"
              :error-messages="errors"
              label="Length"
              outlined
              required
            ></v-text-field>
          </validation-provider>

          <v-btn
            color="success"
            type="submit"
            :disabled="invalid"
            class="mr-2"
            @click="editMovie()"
          >
            Submit
          </v-btn>
        </form>
      </validation-observer>
    </div>
  </div>
</template>

<script>
import { required, numberInt, minValueRule } from "@/helpers/validations";
import {
  ValidationObserver,
  ValidationProvider,
  setInteractionMode,
} from "vee-validate";

setInteractionMode("eager");

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data() {
    return {
      required,
      numberInt,
      selectedActors: [],
      minValueRule,
      cinemaId: null,
      movieId: null,
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
    this.getActors();
  },
  watch: {
    movie() {
      this.selectedActors = this.movie.actors;
    },
  },
  computed: {
    loading() {
      return this.$store.state.movies.loading;
    },
    movie() {
      return this.$store.state.movies.movie;
    },
    actors: {
      get() {
        return this.$store.state.movies.actors;
      },
      set(actors) {
        this.selectedActors = actors;
      },
    },
    allActors() {
      return this.$store.state.actors.actors;
    },
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    getActors() {
      this.$store.dispatch("getActors").catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching movie actors!"
        );
      });
    },
    getMovie(query) {
      this.$store
        .dispatch("getMovie", query)
        .then(() => {
          this.selectedActors = this.movie.actors;
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching movie!"
          );
        });
    },
    editMovie() {
      const actors = [];
      if (this.selectedActors != []) {
        this.selectedActors.forEach((actor) => {
          actors.push(actor.id);
        });
      }

      const movie = {
        id: this.movieId,
        title: this.movie.title,
        description: this.movie.description,
        director: this.movie.director,
        actorIds: actors,
        trailerLink: this.movie.trailerLink,
        releaseYear: this.movie.releaseYear,
        releaseDate: this.movie.releaseDate,
        country: this.movie.country,
        language: this.movie.language,
        genre: this.movie.genre,
        length: this.movie.length,
      };
      this.$store
        .dispatch("editMovie", { cinemaId: this.cinemaId, movie: movie })
        .then(() => {
          this.clear();
          this.$router.push({
            name: "MoviesDashboard",
          });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while creating movies!"
          );
        });
    },

    clear() {
      this.title = "";
      this.description = "";
      this.director = "";
      this.trailerLink = "";
      this.releaseYear = 0;
      this.releaseDate = "";
      this.country = "";
      this.language = "";
      this.genre = "";
      this.length = 0;
      this.$refs.observer.reset();
    },
  },
};
</script>
