<template>
  <v-container>
    <v-card class="pa-5">
      <v-card-title>
        <span class="headline">Add User Manually</span>
      </v-card-title>
      <v-card-subtitle>
        Use this if a user is registered in Firebase but doesn't appear in the list.
        You can find the User ID (UID) in the Firebase Console.
      </v-card-subtitle>
      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="user.id"
            label="User ID (UID from Firebase)"
            required
            outlined
            :rules="[v => !!v || 'UID is required']"
          ></v-text-field>
          <v-text-field
            v-model="user.displayName"
            label="Display Name"
            required
            outlined
            :rules="[v => !!v || 'Name is required']"
          ></v-text-field>
          <v-text-field
            v-model="user.email"
            label="Email"
            required
            outlined
            :rules="[v => !!v || 'Email is required']"
          ></v-text-field>
          <v-checkbox
            v-model="user.isAdmin"
            label="Is Admin?"
          ></v-checkbox>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey" text @click="$router.push({ name: 'UsersDashboard' })">Cancel</v-btn>
        <v-btn color="success" :loading="loading" :disabled="!valid" @click="submit">Create User</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "CreateUser",
  data: () => ({
    valid: false,
    loading: false,
    user: {
      id: "",
      displayName: "",
      email: "",
      photoURL: "",
      isAdmin: false,
    },
  }),
  methods: {
    async submit() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        try {
          await this.$store.dispatch("addUser", this.user);
          this.$router.push({ name: "UsersDashboard" });
        } catch (error) {
          console.error("Error creating user:", error);
          alert("Failed to create user: " + error.message);
        } finally {
          this.loading = false;
        }
      }
    },
  },
};
</script>
