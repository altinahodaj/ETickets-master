<template>
  <body class="profile">
    <div class="container">
      <h2>Account Settings</h2>
      <div class="profile-info">
        <v-avatar size="50">
          <img :src="user.photoURL" />
        </v-avatar>
        <div class="input">
          <label for="firstName">First Name:</label>
          <p>{{ user.displayName }}</p>
        </div>
        <div class="input">
          <label for="email">Email:</label>
          <p>{{ user.email }}</p>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
export default {
  components: {},
  props: {},
  data() {
    return {
      items: ["Cinemas", "Movies", "Events"],
    };
  },
  methods: {},
  computed: {
    user() {
      return this.$store.state.users.user;
    },
  },
};
</script>

<style lang="scss" scoped>
.dark input {
  background: #303030;
}

.dark label {
  color: #f1f1f1;
  font-size: 20px !important;
}

.dark div {
  background: #303030 !important;
}

.profile {
  .container {
    max-width: 1000px;
    padding: 60px 25px;

    h2 {
      text-align: center;
      margin-bottom: 16px;
      font-weight: 300;
      font-size: 32px;
    }

    .profile-info {
      border-radius: 8px;
      box-shadow: 0 4px 6px -1 rgba(0, 0, 0, 0.1),
        0 2px 4px -1px rgba(0, 0, 0, 0.86);
      padding: 32px;
      background-color: #f1f1f1;
      display: flex;
      flex-direction: column;
      max-width: 600px;
      margin: 32px auto;

      .initials {
        position: initial;
        width: 80px;
        height: 80px;
        font-size: 32px;
        background-color: #303030;
        color: #fff;
        display: flex;
        align-self: center;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
      }

      .icon {
        width: 14px;
        height: auto;
        margin-right: 8px;
      }
    }

    .input {
      margin: 16px 0;

      label {
        font-size: 14px;
        display: block;
        padding-bottom: 6px;
      }

      input {
        width: 100%;
        border: none;
        background-color: #f2f7f6;
        padding: 8px;
        height: 50px;

        @media (min-width: 900px) {
        }

        &:focus {
          outline: none;
        }
      }
    }

    button {
      align-self: center;
    }
  }
}
</style>
