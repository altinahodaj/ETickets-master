<template>
  <div class="table-wrapper p-2 cinemas">
    <h2>Actors</h2>
    <hr />
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <div class="d-flex mb-5 cinemas-header">
        <div>
          <v-btn color="success" class="mr-2" @click="onCreateActor()">
            <v-icon left dark> mdi-plus </v-icon>
            Create Actor
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
            :loading="removingActor"
            :disabled="!isSelected || removingActor"
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
          :items="actors"
          item-key="id"
          :items-per-page="10"
          :loading="loading"
          loading-text="Loading Actors... Please wait"
          :class="{ loaded: !loading }"
          class="elevation-1"
        >
          <template v-slot:[`item.fullName`]="{ item }">
            <a class="link" @click="onDetailsClick(item.id)">
              {{ `${item.firstName} ${item.lastName}` }}
            </a>
          </template>
          <template v-slot:[`item.avatar`]="{ item }">
            <v-avatar contain class="ma-2" color="blue">
              <img
                v-if="item.photos.length > 0"
                :src="item.photos[0].imgClientPath"
                :alt="item.id"
                class="avatar-image"
              />
              <img
                v-else
                src="http://localhost:8080/assets/app_files/Movies/default-image.jpg"
                :alt="item.id"
                class="avatar-image"
              />
            </v-avatar>
          </template>
          <template v-slot:[`item.genre`]="{ item }">
            <v-chip class="ma-2" color="primary lighten-2">
              {{ item.genre }}
            </v-chip>
          </template>
          <template v-slot:[`item.birth`]="{ item }">
            <span>{{ formatSimpleDateTime(item.birth) }}</span>
          </template>
          <template #empty>
            <div v-if="loading" class="loading-table text-center py-1">
              <b-spinner variant="primary" />
            </div>
            <template v-else>
              <no-data
                no-data-text="No Actors have been added yet..."
                create-text="+ Add an Actor"
                access-page="Actors"
                @action="onCreateActor()"
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
  name: "Actors",
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
        { text: "Full Name", value: "fullName" },
        { text: "Image", value: "avatar" },
        { text: "Nationality", value: "nationality" },
        { text: "Genre", value: "genre" },
        { text: "Birth", value: "birth" },
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
        { key: "firstName" },
        { key: "lastName" },
        { key: "imgPath" },
        { key: "nationality" },
        { key: "genre" },
        { key: "birth" },
      ],
    };
  },
  computed: {
    loading() {
      return this.$store.state.actors.loading;
    },
    actors() {
      return this.$store.state.actors.actors;
    },
    removingActor() {
      return this.$store.state.actors.removingActor;
    },
    isSelected() {
      return this.selected[0];
    },
  },
  watch: {
    currentPage() {
      this.getActors();
    },
  },
  created() {
    this.getActors();
  },
  methods: {
    onRowSelected(item) {
      this.selected = item;
    },
    onRefresh() {
      this.getActors();
    },
    getActors() {
      this.$store.dispatch("getActors").catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching actors!"
        );
      });
    },
    onEditClick(actorId) {
      this.$router.push({
        name: "actor-edit",
        params: { actorId },
      });
    },
    onDetailsClick(actorId) {
      this.$router.push({
        name: "actor-details",
        params: { actorId },
      });
    },
    onCreateActor() {
      this.$router.push({
        name: "actor-create",
      });
    },
    onDeleteClick(actorId) {
      this.confirmDelete(
        "Delete Actor",
        "Are you sure you want to delete this actor?"
      ).then((ok) => {
        if (ok) {
          this.$store
            .dispatch("removeActor", actorId)
            .then(() => {
              this.selected = [];
              this.getActors();
              this.successToast("Actor was removed");
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
