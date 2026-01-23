<template>
  <div class="table-wrapper p-2 users">
    <v-row>
      <v-col cols="9">
        <h2>Users</h2>
      </v-col>
    </v-row>

    <hr />
    <div class="d-flex mb-5 users-header">
      <div>
        <v-btn color="success" class="mr-2" @click="onCreateUser()">
          <v-icon left dark> mdi-plus </v-icon>
          Add User
        </v-btn>
      </div>
      <div>
        <v-btn
          color="primary"
          :disabled="!isSelected"
          class="mr-2 d-lg-inline action-user-button"
          @click="onEditClick(selected[0].id)"
        >
          Edit
        </v-btn>
        <v-btn
          color="error"
          :loading="loading"
          :disabled="!isSelected || loading"
          class="mr-2 d-lg-inline action-user-button"
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
      <div>
        <v-btn
          color="primary"
          :disabled="!isSelected || selected[0].isAdmin"
          class="mr-2 d-lg-inline action-user-button"
          @click="makeAdmin(selected[0].id)"
        >
          Make Admin
        </v-btn>
      </div>
      <v-btn
        color="error"
        :loading="loading"
        :disabled="!isSelected || !selected[0].isAdmin"
        class="mr-2 d-lg-inline action-user-button"
        @click="removeAdmin(selected[0].id)"
      >
        Remove Admin
        <template v-slot:loader>
          <span class="custom-loader">
            <v-icon light>mdi-cached</v-icon>
          </span>
        </template>
      </v-btn>
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
        :items="users"
        item-key="id"
        :items-per-page="10"
        :loading="loading"
        loading-text="Loading Users... Please wait"
        :class="{ loaded: !loading }"
        class="elevation-1"
      >
        <template v-slot:[`item.id`]="{ item }">
          <a class="link" @click="onDetailsClick(item.id)">{{ item.id }}</a>
        </template>
        <template v-slot:[`item.isAdmin`]="{ item }">
          <v-chip v-if="item.isAdmin" class="ma-2" color="primary">
            Admin
          </v-chip>
          <v-chip v-else class="ma-2"> User </v-chip>
        </template>
        <template slot="no-data">
          <div v-if="loading" class="loading-table text-center py-1">
            <b-spinner variant="primary" />
          </div>
          <template v-else>
            <no-data
              no-data-text="No Movies have been added to this cinema yet..."
              create-text="+ Create Movie"
              access-page="Movies"
              @action="onCreateUser()"
            />
          </template>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "UsersDashboard",
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
        { text: "Display Name", value: "displayName" },
        { text: "Email", value: "email" },
        { text: "Role", value: "isAdmin" },
      ],
      fields: [
        {
          key: "selected",
          label: "",
          variant: "select",
          hide: true,
        },
        { key: "id" },
        { key: "displayName" },
        { key: "email" },
        { key: "isAdmin" },
      ],
    };
  },
  methods: {
    sortBy(prop) {
      this.moviesList.sort((a, b) => (a[prop] < b[prop] ? -1 : 1));
    },
    getUsers() {
      this.$store.dispatch("getUsers").catch((error) => {
        console.log("error", error);
      });
    },
    makeAdmin(id) {
      this.$store
        .dispatch("makeAdmin", id)
        .catch((error) => {
          console.log("error making admin", error);
        })
        .then(() => this.onRefresh());
    },
    removeAdmin(id) {
      this.$store
        .dispatch("removeAdmin", id)
        .catch((error) => {
          console.log("error removing admin", error);
        })
        .then(() => this.onRefresh());
    },
    onRefresh() {
      this.getUsers();
      this.selected = [];
    },
    onEditClick(userId) {
      this.$router.push({
        name: "user-edit",
        params: { userId: userId },
      });
    },
    onDetailsClick(userId) {
      this.$router.push({
        name: "user-details",
        params: { userId: userId },
      });
    },
    onCreateUser() {
      this.$router.push({
        name: "user-create",
      });
    },
    onDeleteClick(userId) {
      this.confirmDelete(
        "Delete User",
        "Are you sure you want to delete this user?"
      ).then((ok) => {
        //TODOS: Fix user delete function later
        if (ok) {
          console.log(userId);
        }
      });
    },
  },
  computed: {
    users() {
      return this.$store.state.users.users;
    },
    loading() {
      return this.$store.state.users.loading;
    },
    isSelected() {
      return this.selected[0];
    },
  },
  created() {
    this.getUsers();
  },
};
</script>
<style scoped></style>
