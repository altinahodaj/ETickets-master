<template>
  <div>
    <h2>Edit Hall</h2>
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
              v-model="hall.name"
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
              v-model="hall.hallNumber"
              :error-messages="errors"
              label="Hall Number"
              outlined
              required
            ></v-text-field>
          </validation-provider>

          <validation-provider name="Trailer Link" rules="required">
            <v-switch
              v-model="hall.has3D"
              :label="`Has 3D Display: ${hall.has3D.toString()}`"
            ></v-switch>
          </validation-provider>

          <v-btn
            color="success"
            type="submit"
            :disabled="invalid"
            class="mr-2"
            @click="editHall()"
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
      hallId: null,
    };
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
    this.hallId = this.$route.params.hallId;
    const query = {
      cinemaId: this.cinemaId,
      hallId: this.hallId,
    };
    this.getHall(query);
  },
  computed: {
    loading() {
      return this.$store.state.halls.loading;
    },
    hall() {
      return this.$store.state.halls.hall;
    },
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    getHall(query) {
      this.$store.dispatch("getHall", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching hall!"
        );
      });
    },
    editHall() {
      const hall = {
        id: this.hallId,
        name: this.hall.name,
        numberOfRows: this.hall.numberOfRows,
        hallNumber: this.hall.hallNumber,
        has3D: this.hall.has3D,
      };
      this.$store
        .dispatch("editHall", { cinemaId: this.cinemaId, hall: hall })
        .then(() => {
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
  },
};
</script>
