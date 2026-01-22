<template>
  <div>
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <div class="container mt-5">
        <v-col class="d-flex align-center justify-content-center" cols="12">
          <div v-if="cinema.photos.length > 0">
            <div class="d-flex justify-content-center flex-wrap w-100">
              <v-carousel>
                <v-carousel-item
                  v-for="(photo, i) in cinema.photos"
                  :key="i"
                  :src="photo.imgClientPath"
                  min-width="1100"
                  max-width="1100"
                  reverse-transition="fade-transition"
                  transition="fade-transition"
                >
                </v-carousel-item>
              </v-carousel>
              <div>
                <v-row>
                  <v-col cols="12">
                    <span
                      >Name:
                      <h4>{{ cinema.name }}</h4>
                    </span>
                  </v-col>
                  <v-col cols="12">
                    <span
                      >Description:
                      <h6>
                        {{ cinema.description | truncate(600, "...") }}
                      </h6>
                    </span>
                  </v-col>

                  <v-col cols="12">
                    <span
                      >Location:
                      <h6>
                        <div class="my-4 text-subtitle-1">
                          <v-icon light>place</v-icon>
                          {{ `${cinema.city}, ${cinema.address}` }}
                        </div>
                      </h6></span
                    >
                  </v-col>
                </v-row>
              </div>
            </div>
          </div>
          <div v-else class="d-flex flex-column mb-5">
            <h2>There are no photos for this cinema!</h2>
          </div>
        </v-col>
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
import { required, numberInt, minValueRule } from "@/helpers/validations";
import { setInteractionMode } from "vee-validate";

setInteractionMode("eager");

export default {
  components: {},
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
  filters: {
    truncate: function (text, length, suffix) {
      if (text.length > length) {
        return text.substring(0, length) + suffix;
      } else {
        return text;
      }
    },
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
      this.$store
        .dispatch("getCinema", cinemaId)
        .then(() => {})
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching cinema!"
          );
        });
    },
  },
};
</script>
