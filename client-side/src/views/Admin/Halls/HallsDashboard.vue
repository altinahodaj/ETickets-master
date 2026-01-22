<template>
  <div class="table-wrapper p-2 halls">
    <v-row>
      <v-col cols="9">
        <h2>Halls</h2>
      </v-col>
      <v-col cols="3">
        <v-select
          solo
          v-model="selectedCinema"
          :items="getObjectOptionsName(cinemas)"
          @change="changeCinema()"
          label="Select Cinema"
        ></v-select>
      </v-col>
    </v-row>

    <hr />
    <div class="d-flex mb-5 halls-header">
      <div>
        <v-btn color="success" class="mr-2" @click="onCreateHall()">
          <v-icon left dark> mdi-plus </v-icon>
          Create Hall
        </v-btn>
      </div>
      <div>
        <v-btn
          color="primary"
          :disabled="!isSelected"
          class="mr-2 d-lg-inline action-hall-button"
          @click="onEditClick(selected[0].id)"
        >
          Edit
        </v-btn>
        <v-btn
          color="error"
          :loading="removingHall"
          :disabled="!isSelected || removingHall"
          class="mr-2 d-lg-inline action-halls-button"
          @click="onDeleteClick(selected[0].id)"
        >
          Delete
          <template v-slot:loader>
            <span class="custom-loader">
              <v-icon light>mdi-cached</v-icon>
            </span>
          </template>
        </v-btn>
      </div>
      <v-btn
        :loading="loading"
        :disabled="loading"
        color="blue-grey"
        class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
        @click="onRefresh()"
      >
        Refresh
        <v-icon right dark> mdi-refresh </v-icon>
        <template v-slot:loader>
          <span class="custom-loader">
            <v-icon light>mdi-cached</v-icon>
          </span>
        </template>
      </v-btn>
    </div>
    <div class="default-table position-relative d-lg-block">
      <v-data-table
        v-model="selected"
        :single-select="true"
        show-select
        :headers="headers"
        :items="halls"
        item-key="id"
        :items-per-page="10"
        :loading="loading"
        loading-text="Loading Halls... Please wait"
        :class="{ loaded: !loading }"
        class="elevation-1"
      >
        <template v-slot:[`item.name`]="{ item }">
          <a class="link" @click="onDetailsClick(item.id)">{{ item.name }}</a>
        </template>
        <template slot="no-data">
          <div v-if="loading" class="loading-table text-center py-1">
            <b-spinner variant="primary" />
          </div>
          <template v-else>
            <no-data
              no-data-text="No Halls have been added to this cinema yet..."
              create-text="+ Create Hall"
              access-page="Halls"
              @action="onCreateHall()"
            />
          </template>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "Halls",
  components: {},
  data() {
    return {
      selected: [],
      headers: [
        {
          text: "Id",
          align: "start",
          sortable: false,
          value: "id",
        },
        { text: "Name", value: "name" },
        { text: "Hall Number", value: "hallNumber" },
        { text: "Number Of Rows", value: "numberOfRows" },
        { text: "Has 3D Display", value: "has3D" },
      ],
      selectedCinema: null,
      fields: [
        {
          key: "selected",
          label: "",
          variant: "select",
          hide: true,
        },
        { key: "id" },
        { key: "name" },
        { key: "hallNumber" },
        { key: "numberOfRows" },
        { key: "has3D" },
      ],
    };
  },
  computed: {
    loading() {
      return this.$store.state.halls.loading;
    },
    halls() {
      return this.$store.state.halls.halls;
    },
    cinemas() {
      return this.$store.state.cinemas.cinemas;
    },
    removingHall() {
      return this.$store.state.halls.removingHall;
    },
    isSelected() {
      return this.selected[0];
    },
  },
  created() {
    this.getCinemas();
  },
  methods: {
    onRefresh() {
      this.getHalls(this.selectedCinema);
    },
    getCinema() {
      this.$store.dispatch("getCinema").catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching cinemas!"
        );
      });
    },
    getCinemas() {
      this.$store
        .dispatch("getCinemas")
        .then(() => {
          if (this.selectedCinema == null) {
            this.selectedCinema = this.cinemas[0];
          }
          this.getHalls(this.selectedCinema);
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching cinemas!"
          );
        });
    },
    getHalls(selectedCinema) {
      this.$store.dispatch("getHalls", selectedCinema.id).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching halls!"
        );
      });
    },
    changeCinema() {
      if (this.selectedCinema != null) {
        this.getHalls(this.selectedCinema);
      }
    },
    onEditClick(hallId) {
      this.$router.push({
        name: "hall-edit",
        params: { cinemaId: this.selectedCinema.id, hallId: hallId },
      });
    },
    onDetailsClick(hallId) {
      this.$router.push({
        name: "hall-details",
        params: { cinemaId: this.selectedCinema.id, hallId: hallId },
      });
    },
    onCreateHall() {
      this.$router.push({
        name: "hall-create",
        params: { cinemaId: this.selectedCinema.id },
      });
    },
    onDeleteClick(hallId) {
      this.confirmDelete(
        "Delete Hall",
        "Are you sure you want to delete this hall?"
      ).then((ok) => {
        if (ok) {
          this.$store
            .dispatch("removeHall", {
              cinemaId: this.selectedCinema.id,
              hallId: hallId,
            })
            .then(() => {
              this.successToast("Hall was removed");
              this.selected = [];
              this.getHalls(this.selectedCinema);
            })
            .catch((error) => {
              this.errorToast(error.response.data.errors[0]);
            });
        }
      });
    },
  },
};
</script>
<style lang="scss" scoped></style>
