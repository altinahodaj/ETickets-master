<template>
  <div>
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <v-row>
        <v-col cols="9">
          <h2>Actor Details</h2>
        </v-col>
        <v-col class="d-flex align-content-end" cols="3">
          <v-btn
            class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
            color="success"
            @click="redirectToAddPhoto(actorId)"
          >
            <v-icon left dark> mdi-camera </v-icon>
            Add Images
          </v-btn>
        </v-col>
      </v-row>

      <hr />
      <div class="container mt-5">
        <v-col class="d-flex align-center justify-content-center" cols="12">
          <v-item v-if="actor.photos.length > 0">
            <v-carousel class="col-6">
              <v-carousel-item
                v-for="(photo, i) in actor.photos"
                :key="i"
                :src="photo.imgClientPath"
                reverse-transition="fade-transition"
                transition="fade-transition"
              >
                <div class="d-flex align-content-end p-3">
                  <v-btn
                    class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
                    color="error"
                    @click="removePhoto(actorId, photo)"
                  >
                    <v-icon left dark> mdi-close </v-icon>
                    Remove
                  </v-btn>
                </div>
              </v-carousel-item>
            </v-carousel>
          </v-item>
          <div v-else class="d-flex flex-column mb-5">
            <h2>There are no photos for this actor!</h2>
            <v-btn
              color="success"
              class="mr-2"
              @click="redirectToAddPhoto(actorId)"
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
                    >First Name:
                    <h6>{{ actor.firstName }}</h6>
                  </span>
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Last Name:
                    <h6>{{ actor.lastName }}</h6></span
                  >
                </v-item>
              </v-col>

              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Image Path:
                    <h6>{{ actor.imgPath }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Nationality:
                    <h6>{{ actor.nationality }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Genre:
                    <h6>{{ actor.genre }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Date of Birth:
                    <h6>{{ actor.birth }}</h6></span
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
      actorId: null,
      cinemaId: 0,
      required,
      numberInt,
      minValueRule,
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
    removePhoto(actorId, photo) {
      this.$store
        .dispatch("removeActorPhoto", {
          cinemaId: 0,
          actorId: actorId,
          photoId: photo.longId,
        })
        .then(() => {
          this.getActor(actorId);
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while deleting photo!"
          );
        });
    },
    getActor(actorId) {
      this.$store
        .dispatch("getActor", actorId)
        .then(() => {})
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching actor!"
          );
        });
    },
    redirectToAddPhoto(actorId) {
      this.$router.push({
        name: "actor-add-photo",
        params: { actorId: actorId },
        //  cinemaId: this.cinemaId,
      });
    },
  },
};
</script>
