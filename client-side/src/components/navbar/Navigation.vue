<template>
  <div class="header">
    <router-link :to="{ name: 'Home' }">
      <img
        src="/assets/main-logo_1.jpg"
        alt="Logo"
        style="height: 40px"
        class="logo-img"
      />
    </router-link>
    <div class="header-right align-middle" style="margin-top: 21px">
      <div class="left">
        <router-link
          :class="routeName == 'Home' && 'active'"
          :to="{ name: 'Home' }"
        >
          Home
        </router-link>
        <router-link
          :class="routeName == 'Events' && 'active'"
          :to="{ name: 'Events' }"
        >
          Events
        </router-link>
        <router-link
          :class="routeName == 'Movies' && 'active'"
          :to="{ name: 'Movies' }"
        >
          Movies
        </router-link>
        <router-link
          :class="routeName == 'Cinemas' && 'active'"
          :to="{ name: 'Cinemas' }"
        >
          Cinemas
        </router-link>

        <!-- ✅ Admin Dashboard Button -->
        <router-link
          v-if="isAdmin"
          class="admin-btn"
          :to="{ name: 'Admin' }"
        >
          <v-icon left color="white">mdi-shield-account</v-icon>
          Admin Dashboard
        </router-link>

        <div class="hidethese2">
          <router-link v-if="isAdmin" :to="{ name: 'Admin' }">
            Admin
          </router-link>
          <router-link
            v-if="isLoggedIn && user.displayName"
            class="link"
            :to="{ name: 'Profile' }"
          >
            {{ user.displayName }}
          </router-link>
          <router-link
            v-if="isLoggedIn"
            @click="handleSignOut()"
            :to="{ name: 'Login' }"
          >
            Sign Out
          </router-link>
        </div>
        <v-select
          solo
          v-model="selectedCinema"
          :items="getObjectOptionsName(cinemas)"
          @change="changeCinema()"
          label="Select Cinema"
        ></v-select>
      </div>

      <div class="right">
        <v-btn
          outlined
          text
          v-if="!isLoggedIn"
          :class="routeName == 'Login' && 'active'"
          :to="{ name: 'Login' }"
          class="mr-2"
        >
          <span>Login</span>
          <v-icon right>login</v-icon>
        </v-btn>
        <v-btn
          outlined
          text
          v-if="!isLoggedIn"
          :class="routeName == 'Register' && 'active'"
          :to="{ name: 'Register' }"
          class="mr-2"
        >
          <span>Sign Up</span>
          <v-icon right>person_add</v-icon>
        </v-btn>
        <div v-if="isLoggedIn" class="hidethis">
          {{ user.displayName }}
          <v-avatar size="50">
            <img :src="user.photoURL" />
          </v-avatar>
        </div>
        <div class="hideDrawer">
          <v-app-bar-nav-icon
            v-if="isLoggedIn"
            @click.stop="drawer = !drawer"
          ></v-app-bar-nav-icon>
        </div>
        <v-navigation-drawer v-model="drawer" absolute bottom temporary>
          <v-list nav dense>
            <v-list-item-group
              v-model="group"
              active-class="deep-purple--text text--accent-4"
            >
              <v-list-item>
                <v-list-item-title>
                  <router-link v-if="isAdmin" :to="{ name: 'Admin' }">
                    Admin
                  </router-link>
                </v-list-item-title>
              </v-list-item>

              <v-list-item>
                <v-list-item-title>
                  <router-link
                    v-if="isLoggedIn"
                    class="link"
                    :to="{ name: 'MyTickets' }"
                  >
                    My Tickets
                  </router-link>
                </v-list-item-title>
              </v-list-item>

              <v-list-item>
                <v-list-item-title>
                  <router-link
                    v-if="isLoggedIn"
                    class="link"
                    :to="{ name: 'Profile' }"
                  >
                    {{ user.displayName }}
                  </router-link>
                </v-list-item-title>
              </v-list-item>
            </v-list-item-group>

            <v-list-item v-if="isLoggedIn">
              <v-list-item-title @click="handleSignOut()">
                <router-link :to="{ name: 'Login' }"> Sign Out </router-link>
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </div>
    </div>
  </div>
</template>

<script>
import { signOut } from "firebase/auth";

export default {
  components: {},
  data() {
    return {
      selectedCinema: null,
      drawer: false,
      group: null,
    };
  },
  props: {
    isLoggedIn: {
      required: true,
      type: Boolean,
    },
    auth: {
      required: true,
    },
  },
  created() {
    this.getCinemas();
  },
  watch: {
    group() {
      this.drawer = false;
    },
  },
  methods: {
    changeCinema() {
      this.$store
        .dispatch("getCinema", this.selectedCinema.id)
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching cinema!"
          );
        });
    },
    handleSignOut() {
      if (!this.auth) {
        this.$router.push("/login");
        return;
      }

      signOut(this.auth).then(() => {
        this.$store.commit("RESET_STATE");
        this.$router.push("/login");
        window.location.reload();
      });
    },
    getCinemas() {
      this.$store
        .dispatch("getCinemas")
        .then(() => {
          if (this.selectedCinema == null) {
            this.selectedCinema = this.cinemas[0];
          }
          // this.getEvents(this.selectedCinema);
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching events!"
          );
        });
    },
  },
  computed: {
    routeName() {
      return this.$route.name;
    },
    user() {
      return this.$store.state.users.user || {};
    },
    isAdmin() {
      return Boolean(this.$store.state.users.isAdmin || this.user.isAdmin);
    },
    cinemas() {
      return this.$store.state.cinemas.cinemas || [];
    },
  },
};
</script>

<style lang="scss" scoped>
.logo-img {
  max-width: 250px;
}
.header-right {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;

  .right {
    height: 80px;
  }
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.header {
  overflow: hidden;
  background-color: rgb(72, 143, 239);
  padding: 20px 10px;
  width: 100%;
  display: flex;
  flex-direction: row;
}

.header a {
  float: left;
  color: black;
  text-align: center;
  padding: 12px;
  text-decoration: none;
  font-size: 18px;
  line-height: 25px;
  border-radius: 4px;
  font-family: "Ubuntu", sans-serif;
}

.header a.logo {
  font-size: 35px;
  font-weight: bold;
}

.header a:hover {
  background-color: white;
  color: black;
}

.header a.active {
  background-color: rgb(33, 31, 32);
  color: white;
}

.header-right {
  padding: 1px;
}

.hidethese2 {
  display: none;
}

@media only screen and (max-width: 600px) {
  img {
    display: none;
  }
  .hidethis {
    display: none;
  }

  .hidethese2 {
    display: block;
  }

  .hideDrawer {
    display: none;
  }

  .header a {
    float: none;
    display: block;
    text-align: left;
  }

  .header-right {
    float: none;
  }
}
</style>
