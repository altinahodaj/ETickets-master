<template>
  <div>
    <v-row>
      <h2 class="pl-5">Create Movie Times</h2>
    </v-row>
    <hr />
    <div class="container mt-5">
      <validation-observer ref="observer" v-slot="{ invalid }">
        <form @submit.prevent="submit">
          <validation-provider
            v-slot="{ errors }"
            name="Start Time"
            rules="required"
          >
            <v-select
              solo
              :error-messages="errors"
              v-model="selectedHall"
              :items="getObjectOptionsName(halls)"
              label="Select Hall"
            ></v-select>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Start Time"
            rules="required"
          >
            <v-text-field
              v-model="startTime"
              type="datetime-local"
              :error-messages="errors"
              label="Start Time"
              :min="formatShortDateTime(new Date())"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="End Time"
            rules="required"
          >
            <v-text-field
              v-model="endTime"
              type="datetime-local"
              :error-messages="errors"
              label="End Time"
              outlined
              :min="startTime"
              required
            ></v-text-field>
          </validation-provider>
          <v-btn
            color="success"
            type="submit"
            :disabled="invalid"
            class="mr-2"
            @click="createMovieTime()"
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
      minValueRule,
      cinemaId: null,
      movieId: null,
      startTime: null,
      endTime: null,
      selectedHall: null,
      items: ["Foo", "Bar", "Fizz", "Buzz"],
    };
  },
  computed: {
    halls() {
      return this.$store.state.halls.halls;
    },
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
    this.movieId = this.$route.params.movieId;
    this.getHalls();
  },
  methods: {
    onRefresh() {
      this.getHalls();
    },
    submit() {
      this.$refs.observer.validate();
    },
    getHalls() {
      this.$store.dispatch("getHalls", this.cinemaId).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching Halls!"
        );
      });
    },
    createMovieTime() {
      const movieTime = {
        hallId: this.selectedHall.id,
        startTime: this.startTime,
        endTime: this.endTime,
      };
      this.$store
        .dispatch("createMovieTime", {
          cinemaId: this.cinemaId,
          movieId: this.movieId,
          movieTime: movieTime,
        })
        .then(() => {
          this.clear();
          this.$router.push({
            name: "MoviesDashboard",
          });
        })
        .catch((error) => {
          console.log(error);
          this.errorToast(
            error.response?.data ||
              "Something went wrong while creating movie times!"
          );
        });
    },
    clear() {
      this.selectedHall = null;
      this.startTime = null;
      this.endTime = null;
      this.$refs.observer.reset();
    },
  },
};
</script>
