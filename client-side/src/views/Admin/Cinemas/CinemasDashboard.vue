<template>
  <div class="table-wrapper p-2 cinemas">
    <h2>Cinemas</h2>
    <hr />
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <div class="d-flex mb-5 cinemas-header">
        <div>
          <v-btn color="success" class="mr-2" @click="onCreateCinema()">
            <v-icon left dark> mdi-plus </v-icon>
            Create Cinema
          </v-btn>
        </div>
        <div>
          <v-btn
            color="primary"
            :disabled="!isSelected"
            class="mr-2 d-lg-inline action-cinema-button"
            @click="onEditClick(selected[0].id)"
          >
            Edit
          </v-btn>
          <v-btn
            color="error"
            :loading="removingCinema"
            :disabled="!isSelected || removingCinema"
            class="mr-2 d-lg-inline action-cinema-button"
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
          :items="cinemas"
          item-key="id"
          :items-per-page="10"
          :loading="loading"
          loading-text="Loading Cinemas... Please wait"
          :class="{ loaded: !loading }"
          class="elevation-1"
        >
          <template v-slot:[`item.name`]="{ item }">
            <a class="link" @click="onDetailsClick(item.id)">{{ item.name }}</a>
          </template>
          <template v-slot:[`item.image`]="{ item }">
            <v-avatar tile contain class="ma-2" color="blue">
              <img
                v-if="item.photos.length > 0"
                :src="item.photos[0].imgClientPath"
                :alt="item.id"
                class="avatar-image"
              />
              <img
                v-else
                src="/assets/app_files/Movies/default-image.jpg"
                :alt="item.id"
                class="avatar-image"
              />
            </v-avatar>
          </template>
          <template #empty>
            <div v-if="loading" class="loading-table text-center py-1">
              <b-spinner variant="primary" />
            </div>
            <template v-else>
              <no-data
                no-data-text="No Cinemas have been added yet..."
                create-text="+ Create Cinema"
                access-page="Cinemas"
                @action="onCreateCinema()"
              />
            </template>
          </template>
        </v-data-table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Cinemas",
  components: {},
  data() {
    return {
      headers: [
        {
          text: "Id",
          align: "start",
          sortable: false,
          value: "id",
        },
        { text: "Name", value: "name" },
        { text: "Image", value: "image" },
        { text: "City", value: "city" },
        { text: "Address", sortable: false, value: "address" },
        { text: "Number Of Venues", value: "numberOfVenues" },
      ],
      selected: [],
      fields: [
        {
          key: "selected",
          label: "",
          variant: "select",
          hide: true,
        },
        { key: "id" },
        { key: "name" },
        { key: "city" },
        { key: "address" },
        { key: "numberOfVenues" },
      ],
    };
  },
  computed: {
    loading() {
      return this.$store.state.cinemas.loading;
    },
    cinemas() {
      return this.$store.state.cinemas.cinemas;
    },
    removingCinema() {
      return this.$store.state.cinemas.removingCinema;
    },
    isSelected() {
      return this.selected[0];
    },
  },
  watch: {
    currentPage() {
      this.getCinemas();
    },
  },
  created() {
    this.getCinemas();
  },
  methods: {
    onRowSelected(item) {
      this.selected = item;
    },
    onRefresh() {
      this.getCinemas();
    },
    getCinemas() {
      this.$store.dispatch("getCinemas").catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching cinemas!"
        );
      });
    },
    onEditClick(cinemaId) {
      this.$router.push({
        name: "cinema-edit",
        params: { cinemaId },
      });
    },
    onDetailsClick(cinemaId) {
      this.$router.push({
        name: "cinema-details",
        params: { cinemaId },
      });
    },
    onCreateCinema() {
      this.$router.push({
        name: "cinema-create",
      });
    },
    onDeleteClick(cinemaId) {
      this.confirmDelete(
        "Delete Cinema",
        "Are you sure you want to delete this cinema?"
      ).then((ok) => {
        if (ok) {
          this.$store
            .dispatch("removeCinema", cinemaId)
            .then(() => {
              this.selected = [];
              this.getCinemas();
              this.successToast("Cinema was removed");
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
