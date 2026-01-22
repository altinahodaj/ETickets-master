<template>
  <v-app>
    <public-layout
      v-if="!isAdminDashboard"
      :isLoggedIn="isLoggedIn"
      :auth="auth"
    >
    </public-layout>
    <dashboard-layout v-else :isLoggedIn="isLoggedIn" :auth="auth">
    </dashboard-layout>
    <v-main class="ma-4" v-if="isAdminDashboard">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import PublicLayout from "@/layouts/Public/PublicLayout.vue";
import DashboardLayout from "@/layouts/Dashboard/DashboardLayout.vue";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import "firebase/auth";
export default {
  components: { PublicLayout, DashboardLayout },
  name: "App",

  data() {
    return {
      isAdmin: false,
      isLoggedIn: false,
      auth: null,
    };
  },
  computed: {
    isAdminDashboard() {
      return this.$route.meta.layout === "dashboard";
    },
  },
  created() {
    this.auth = getAuth();
    onAuthStateChanged(this.auth, (user) => {
      if (user) {
        this.isLoggedIn = true;
      } else {
        this.isLoggedIn = false;
      }
    });
  },
};
</script>

<style lang="scss">
.container {
  padding: 0;
}
</style>
