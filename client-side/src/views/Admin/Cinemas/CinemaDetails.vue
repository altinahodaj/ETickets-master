<template>
  <div>
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <v-row>
        <v-col cols="9">
          <h2>Cinema Details</h2>
        </v-col>
        <v-col class="d-flex align-content-end" cols="3">
          <v-btn
            class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
            color="success"
            @click="redirectToAddPhoto(cinemaId)"
          >
            <v-icon left dark> mdi-camera </v-icon>
            Add Images
          </v-btn>
        </v-col>
      </v-row>

      <hr />
      <div class="container mt-5">
        <v-col class="d-flex align-center justify-content-center" cols="12">
          <v-item v-if="cinema.photos.length > 0">
            <v-carousel>
              <v-carousel-item
                v-for="(photo, i) in cinema.photos"
                :key="i"
                :src="photo.imgClientPath"
                reverse-transition="fade-transition"
                transition="fade-transition"
              >
                <div class="d-flex align-content-end p-3">
                  <v-btn
                    class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
                    color="error"
                    @click="removePhoto(cinemaId, photo)"
                  >
                    <v-icon left dark> mdi-close </v-icon>
                    Remove
                  </v-btn>
                </div>
              </v-carousel-item>
            </v-carousel>
          </v-item>
          <div v-else class="d-flex flex-column mb-5">
            <h2>There are no photos for this cinema!</h2>
            <v-btn
              color="success"
              class="mr-2"
              @click="redirectToAddPhoto(cinemaId)"
            >
              <v-icon left dark> mdi-camera </v-icon>
              Add Image
            </v-btn>
          </div>
        </v-col>

        <v-item-group active-class="primary">
          <v-container>
            <v-row>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Name:
                    <h6>{{ cinema.name }}</h6>
                  </span>
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Number Of Venues:
                    <h6>{{ cinema.numberOfVenues }}</h6></span
                  >
                </v-item>
              </v-col>

              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >City:
                    <h6>{{ cinema.city }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Address:
                    <h6>{{ cinema.address }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Description:
                    <h6>{{ cinema.description }}</h6></span
                  >
                </v-item>
              </v-col>
            </v-row>
          </v-container>
        </v-item-group>
        <div></div>
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
    removePhoto(cinemaId, photo) {
      this.$store
        .dispatch("removeCinemaPhoto", {
          cinemaId: cinemaId,
          photoId: photo.longId,
        })
        .then(() => {
          this.getCinema(cinemaId);
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while deleting photo!"
          );
        });
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
    redirectToAddPhoto(cinemaId) {
      this.$router.push({
        name: "cinema-add-photo",
        cinemaId: cinemaId,
      });
    },
  },
};
</script>
