<template>
  <div>
    <h2>Create Cinema</h2>
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
              v-model="name"
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
              v-model="description"
              :error-messages="errors"
              label="Description"
              outlined
              required
            ></v-textarea>
          </validation-provider>
          <validation-provider v-slot="{ errors }" name="City" rules="required">
            <v-text-field
              v-model="city"
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
              v-model="address"
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
              v-model.number="numberOfVenues"
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
            @click="createCinema()"
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
      name: "",
      description: "",
      city: "",
      address: "",
      numberOfVenues: 0,
    };
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    createCinema() {
      const cinema = {
        name: this.name,
        description: this.description,
        city: this.city,
        address: this.address,
        numberOfVenues: this.numberOfVenues,
      };
      this.$store
        .dispatch("createCinema", cinema)
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
      this.numberOfVenues = 0;
      this.$refs.observer.reset();
    },
  },
};
</script>
