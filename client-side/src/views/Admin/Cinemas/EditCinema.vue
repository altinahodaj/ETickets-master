<template>
  <div>
    <h2>Edit Cinema</h2>
    <hr />
    <div class="container mt-5">
      <validation-observer ref="observer" v-slot="{ invalid }">
        <form @submit.prevent="submit">
          <validation-provider
            v-slot="{ errors }"
            name="Name"
            rules="required|min:3"
          >
            <v-text-field
              v-model="cinema.name"
              :error-messages="errors"
              label="Name"
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
              v-model="cinema.description"
              :error-messages="errors"
              label="Description"
              outlined
              required
            ></v-textarea>
          </validation-provider>
          <validation-provider v-slot="{ errors }" name="City" rules="required">
            <v-text-field
              v-model="cinema.city"
              :error-messages="errors"
              label="City"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Address"
            rules="required"
          >
            <v-text-field
              v-model="cinema.address"
              :error-messages="errors"
              label="Address"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Number Of Venues"
            rules="required"
          >
            <v-text-field
              v-model.number="cinema.numberOfVenues"
              type="number"
              :error-messages="errors"
              label="Number Of Venues"
              outlined
              required
            ></v-text-field>
          </validation-provider>

          <v-btn
            color="success"
            type="submit"
            :disabled="invalid"
            class="mr-2"
            @click="editCinema()"
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
      cinemaId: null,
      required,
      numberInt,
      minValueRule,
    };
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
    this.getCinema(this.cinemaId);
  },
  computed: {
    loading() {
      return this.$store.state.cinemas.loading;
    },
    cinema() {
      return this.$store.state.cinemas.cinema;
    },
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    getCinema(cinemaId) {
      this.$store.dispatch("getCinema", cinemaId).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching cinema!"
        );
      });
    },
    editCinema() {
      const cinema = {
        id: this.cinemaId,
        name: this.cinema.name,
        description: this.cinema.description,
        city: this.cinema.city,
        address: this.cinema.address,
        numberOfVenues: this.cinema.numberOfVenues,
      };
      this.$store
        .dispatch("editCinema", cinema)
        .then(() => {
          this.clear();
          this.$router.push({
            name: "CinemasDashboard",
          });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while creating cinemas!"
          );
        });
    },
    clear() {
      this.name = "";
      this.description = "";
      this.city = "";
      this.address = "";
      this.numOfVenues = 0;
      this.$refs.observer.reset();
    },
  },
};
</script>
