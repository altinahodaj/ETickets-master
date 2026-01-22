<template>
  <div>
    <h2>Create Hall</h2>
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
            name="Hall Number"
            rules="required"
          >
            <v-text-field
              v-model="hallNumber"
              :error-messages="errors"
              label="Hall Number"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider name="Trailer Link" rules="required">
            <v-switch
              v-model="has3D"
              :label="`Has 3D Display: ${has3D.toString()}`"
            ></v-switch>
          </validation-provider>

          <v-btn
            color="success"
            type="submit"
            :disabled="invalid"
            class="mr-2"
            @click="createHall()"
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
      name: "",
      hallNumber: "",
      numberOfRows: 10,
      has3D: false,
    };
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    createHall() {
      const hall = {
        name: this.name,
        hallNumber: this.hallNumber,
        numberOfRows: this.numberOfRows,
        has3D: this.has3D,
      };
      this.$store
        .dispatch("createHall", { cinemaId: this.cinemaId, hall: hall })
        .then(() => {
          this.clear();
          this.$router.push({
            name: "HallsDashboard",
          });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while creating halls!"
          );
        });
    },
    clear() {
      this.name = "";
      this.hallNumber = "";
      this.numberOfRows = 10;
      this.has3D = false;
      this.$refs.observer.reset();
    },
  },
};
</script>
