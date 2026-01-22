<template>
  <div>
    <h2>Create Events</h2>
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
          <validation-provider v-slot="{ errors }" name="date" rules="required">
            <v-text-field
              v-model="date"
              type="datetime-local"
              name=""
              :error-messages="errors"
              label="Event Date"
              outlined
              required
            ></v-text-field>
            <v-text-field
              v-model="price"
              type="number"
              name=""
              :error-messages="errors"
              label="Price"
              outlined
            ></v-text-field>
            <v-text-field
              v-model="attendeesNumber"
              type="number"
              name=""
              :error-messages="errors"
              label="Attendees"
              outlined
            ></v-text-field>
            <v-switch
              v-model="isPaid"
              :label="`Is Paid?`"
            ></v-switch>
          </validation-provider>
          <v-btn
            color="success"
            type="submit"
            :disabled="invalid"
            class="mr-2"
            @click="createEvent()"
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
      name: "",
      description: "",
      date: "date",
      isPaid: "",
      price:"",
      attendeesNumber:"",
    };
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
  },
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    createEvent() {
      const event = {
        name: this.name,
        description: this.description,
        date: this.date,
        isPaid: this.isPaid,
        price:this.price,
      };
      this.$store
        .dispatch("createEvent", { cinemaId: this.cinemaId, event: event })
        .then(() => {
          this.clear();
          this.$router.push({
            name: "EventsDashboard",
          });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while creating events!"
          );
        });
    },
    clear() {
      this.name = "";
      this.description = "";
      this.date = "";
      this.isPaid = "";
      this.price="",
      this.attendeesNumber="",
      this.$refs.observer.reset();
    },
  },
};
</script>
