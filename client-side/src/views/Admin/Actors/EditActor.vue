<template>
  <div>
    <h2>Edit Actor</h2>
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
              v-model="actor.firstName"
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
              v-model="actor.lastName"
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
              v-model="actor.nationality"
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
              v-model="actor.genre"
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
              v-model="actor.birth"
              type="datetime-local"
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
            @click="editActor()"
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
      actorId: null,
    };
  },
  created() {
    this.actorId = this.$route.params.actorId;
    this.getActor(this.actorId);
  },
  computed: {
    loading() {
      return this.$store.state.actors.loading;
    },
    actor() {
      return this.$store.state.actors.actor;
    },
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    getActor(actorId) {
      this.$store.dispatch("getActor", actorId).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching actor!"
        );
      });
    },
    editActor() {
      const actor = {
        id: this.actorId,
        firstName: this.actor.firstName,
        lastName: this.actor.lastName,
        imgPath: this.actor.imgPath,
        nationality: this.actor.nationality,
        genre: this.actor.genre,
        birth: this.actor.birth,
      };
      this.$store
        .dispatch("editActor", actor)
        .then(() => {
          this.clear();
          this.$router.push({
            name: "ActorsDashboard",
          });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while creating actors!"
          );
        });
    },
    clear() {
      (this.firstname = ""),
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
