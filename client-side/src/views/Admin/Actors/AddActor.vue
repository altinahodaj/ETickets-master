<template>
  <div>
    <h2>Add an Actor</h2>
    <hr />
    <div class="container mt-5">
      <validation-observer ref="observer" v-slot="{ invalid }">
        <form @submit.prevent="submit">
          <validation-provider
            v-slot="{ errors }"
            name="First Name"
            rules="required|min:3"
          >
            <v-text-field
              v-model="firstName"
              :error-messages="errors"
              label="First Name"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Last Name"
            rules="required"
          >
            <v-text-field
              v-model="lastName"
              :error-messages="errors"
              label="Last Name"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Nationality"
            rules="required"
          >
            <v-text-field
              v-model="nationality"
              :error-messages="errors"
              label="Nationality"
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
              v-model="genre"
              :error-messages="errors"
              label="Genre"
              outlined
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Birth"
            rules="required"
          >
            <v-text-field
              v-model="birth"
              type="date"
              :error-messages="errors"
              label="Birth"
              outlined
              required
            ></v-text-field>
          </validation-provider>

          <v-btn
            color="success"
            type="submit"
            :disabled="invalid"
            class="mr-2"
            @click="addActor()"
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
      id: 2,
      firstName: "",
      lastName: "",
      imgPath: "",
      nationality: "",
      genre: "",
      birth: "",
    };
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    addActor() {
      const actor = {
        firstName: this.firstName,
        lastName: this.lastName,
        imgPath: this.imgPath,
        nationality: this.nationality,
        genre: this.genre,
        birth: this.birth,
      };
      this.$store
        .dispatch("addActor", actor)
        .then(() => {
          this.clear();
          this.$router.push({
            name: "ActorsDashboard",
          });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while adding Actors!"
          );
        });
    },
    clear() {
      (this.firstName = ""),
        (this.lastName = ""),
        (this.imgPath = ""),
        (this.nationality = ""),
        (this.genre = ""),
        (this.birth = ""),
        this.$refs.observer.reset();
    },
  },
};
</script>
