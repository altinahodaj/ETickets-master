<template>
  <div>
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <v-row>
        <v-col cols="9">
          <h2>Hall Details</h2>
        </v-col>
        <v-col class="d-flex align-content-end" cols="3">
          <v-btn
            class="mt-1 mt-sm-0 ml-auto mr-2 white--text"
            color="primary"
            :loading="generatingSeating"
            @click="seatingDialog = true"
          >
            <v-icon left dark> mdi-seat </v-icon>
            Generate Seating
          </v-btn>
          <v-btn
            class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
            color="success"
            @click="redirectToAddPhoto(cinemaId, hallId)"
          >
            <v-icon left dark> mdi-camera </v-icon>
            Add Images
          </v-btn>
        </v-col>
      </v-row>

      <v-dialog v-model="seatingDialog" max-width="560">
        <v-card>
          <v-card-title class="headline">Generate seating</v-card-title>
          <v-card-text>
            <div class="mb-4">
              This will create rows and seats for this hall (only if it has none).
            </div>
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model.number="seating.rows"
                  type="number"
                  label="Rows"
                  min="1"
                  outlined
                  dense
                />
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model.number="seating.seatsPerRow"
                  type="number"
                  label="Seats per row"
                  min="1"
                  outlined
                  dense
                />
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="seatingDialog = false">Cancel</v-btn>
            <v-btn
              color="primary"
              class="white--text"
              :loading="generatingSeating"
              @click="onGenerateSeating"
            >
              Generate
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <hr />
      <div class="container mt-5">
        <v-col class="d-flex align-center justify-content-center" cols="12">
          <!-- <v-item v-if="hall.photos.length > 0">
            <v-carousel>
              <v-carousel-item
                v-for="(photo, i) in hall.photos"
                :key="i"
                :src="photo.imgClientPath"
                reverse-transition="fade-transition"
                transition="fade-transition"
              >
                <div class="d-flex align-content-end p-3">
                  <v-btn
                    class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
                    color="error"
                    @click="removePhoto(cinemaId, hallId, photo)"
                  >
                    <v-icon left dark> mdi-close </v-icon>
                    Remove
                  </v-btn>
                </div>
              </v-carousel-item>
            </v-carousel>
          </v-item> -->
          <div class="d-flex flex-column mb-5">
            <h2>There are no photos for this hall!</h2>
            <v-btn
              color="success"
              class="mr-2"
              @click="redirectToAddPhoto(cinemaId, hallId)"
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
                    <h6>{{ hall.name }}</h6>
                  </span>
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Hall Number:
                    <h6>{{ hall.hallNumber }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Number Of Rows:
                    <h6>{{ hall.numberOfRows }}</h6></span
                  >
                </v-item>
              </v-col>
              <v-col cols="12" md="4">
                <v-item>
                  <span
                    >Has 3D Display:
                    <h6>{{ hall.has3D }}</h6></span
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
import api from "@/libs/api";
import { required, numberInt, minValueRule } from "@/helpers/validations";
import { setInteractionMode } from "vee-validate";

setInteractionMode("eager");

export default {
  components: {},
  data() {
    return {
      cinemaId: null,
      hallId: null,
      seatingDialog: false,
      generatingSeating: false,
      seating: {
        rows: 5,
        seatsPerRow: 10,
      },
      required,
      numberInt,
      minValueRule,
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
    removePhoto(cinemaId, hallId, photo) {
      this.$store
        .dispatch("removeHallPhoto", {
          cinemaId: cinemaId,
          hallId: hallId,
          photoId: photo.longId,
        })
        .then(() => {
          this.getHall({ cinemaId: cinemaId, hallId: hallId });
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while deleting photo!"
          );
        });
    },
    getHall(query) {
      this.$store.dispatch("getHall", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching hall!"
        );
      });
    },
    redirectToAddPhoto(cinemaId, hallId) {
      this.$router.push({
        name: "hall-add-photo",
        params: { cinemaId: cinemaId, hallId: hallId },
      });
    },

    async onGenerateSeating() {
      const rows = Number(this.seating.rows);
      const seatsPerRow = Number(this.seating.seatsPerRow);

      if (!rows || rows < 1 || !seatsPerRow || seatsPerRow < 1) {
        this.errorToast("Please provide valid rows and seats per row.");
        return;
      }

      this.generatingSeating = true;
      try {
        await api("movies").post(
          `cinemas/${this.cinemaId}/halls/${this.hallId}/generate-seating`,
          {
            rows,
            seats_per_row: seatsPerRow,
          }
        );
        this.successToast("Seating generated successfully!");
        this.seatingDialog = false;
        this.getHall({ cinemaId: this.cinemaId, hallId: this.hallId });
      } catch (error) {
        this.errorToast(
          error.response?.data?.errors?.[0] ||
            error.response?.data?.detail ||
            "Something went wrong while generating seating!"
        );
      } finally {
        this.generatingSeating = false;
      }
    },
  },
};
</script>
