<template>
  <v-container>
    <v-card class="pa-5" :loading="loading">
      <v-card-title>
        <span class="headline">Edit User</span>
      </v-card-title>
      <v-card-text v-if="user">
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="user.id"
            label="User ID"
            readonly
            disabled
            outlined
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
        <v-btn color="primary" :loading="submitting" :disabled="!valid" @click="submit">Update User</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import api from "@/libs/api";

export default {
  name: "EditUser",
  data: () => ({
    valid: false,
    loading: false,
    submitting: false,
    user: null,
  }),
  async created() {
    this.loading = true;
    const userId = this.$route.params.userId;
    try {
      const response = await api("node").get(`users/${userId}`);
      this.user = response.data;
    } catch (error) {
      console.error("Error fetching user:", error);
      alert("User not found");
      this.$router.push({ name: "UsersDashboard" });
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async submit() {
      if (this.$refs.form.validate()) {
        this.submitting = true;
        try {
          await api("node").put(`users/${this.user.id}`, this.user);
          this.$router.push({ name: "UsersDashboard" });
        } catch (error) {
          console.error("Error updating user:", error);
          alert("Update failed");
        } finally {
          this.submitting = false;
        }
      }
    },
  },
};
</script>
