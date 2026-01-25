<template>
  <body class="d-flex justify-content-center form-wrap">
    <v-form ref="form" v-model="valid" lazy-validation>
      <div class="mb-2">
        <h2 class="mb-5">Login to your CinemaVerse Account</h2>
      </div>

      <div class="google-button mb-4">
        <v-btn block color="primary" x-large @click.prevent="signInWithGoogle">
          <v-avatar size="40">
            <img :src="google" />
          </v-avatar>
          <span class="ml-5"> Sign In With Google </span>
        </v-btn>
        <v-btn fab icon> </v-btn>
      </div>

      <v-row wrap no-gutters>
        <v-col cols="12" class="text-center">
          <v-divider vertical />
        </v-col>
        <v-col cols="12" class="text-center"> <h3>Or</h3> </v-col>
        <v-col cols="12" class="text-center mb-4">
          <v-divider vertical />
        </v-col>
      </v-row>
      <v-text-field
        type="text"
        placeholder="Email"
        v-model="email"
        :rules="emailRules"
        prepend-inner-icon="email"
        label="E-mail"
        required
        outlined
      />

      <v-text-field
        v-model="password"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[rules.required]"
        :type="show1 ? 'text' : 'password'"
        name="input-10-1"
        prepend-inner-icon="key"
        label="Password"
        outlined
        @click:append="show1 = !show1"
      />
      <div v-if="errorMsg">
        <h6 class="error--text">
          {{ errorMsg }}
        </h6>
      </div>
      <div class="my-2">
        <v-btn
          block
          large
          :disabled="!valid"
          color="success"
          @click.prevent="submitForm"
        >
          Submit
        </v-btn>
      </div>
      <hr />
      <div class="noAcc">
        <p>
        Don't have an account?
        </p>
        <v-btn outlined color="primary" :to="{ name: 'Register' }">
          Register
        </v-btn>
      </div>
    </v-form>
  </body>
</template>

<script>
import {
  getAuth,
  signInWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
} from "firebase/auth";
export default {
  data() {
    return {
      google: require("@/assets/google-logo2.png"),
      valid: false,
      show1: false,
      emailRules: [
        (v) => !!v || "E-mail is required",
        (v) => /.+@.+/.test(v) || "E-mail must be valid",
      ],

      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => v.length >= 8 || "Min 8 characters",
      },
      email: null,
      password: null,
      errorMsg: null,
    };
  },

  methods: {
    signInWithGoogle() {
      const provider = new GoogleAuthProvider();
      signInWithPopup(getAuth(), provider).then((result) => {
        this.getUserSync(result.user).finally(() => {
          const isAdmin = Boolean(this.$store.state.users.user?.isAdmin);
          this.$router.push(isAdmin ? "/admin" : "/home");
        });
      });
    },
    getUserSync(fbUser) {
      return this.$store.dispatch("getUser", fbUser.uid).catch((error) => {
        if (error.response && error.response.status === 404) {
          console.log("User not in SQL DB, syncing...");
          const newUser = {
            id: fbUser.uid,
            email: fbUser.email,
            username: fbUser.displayName || fbUser.email.split("@")[0],
          };
          return this.$store.dispatch("addUser", newUser);
        }
        console.error("getUser error:", error);
      });
    },
    validate() {
      this.$refs.form.validate();
    },
    submitForm() {
      this.validate;
      if (this.isFormValid()) {
        this.errorMsg = null;
        signInWithEmailAndPassword(getAuth(), this.email, this.password)
          .then((result) => {
            this.getUserSync(result.user).finally(() => {
              const isAdmin = Boolean(this.$store.state.users.user?.isAdmin);
              this.$router.push(isAdmin ? "/admin" : "/home");
            });
          })
          .catch((err) => {
            this.errorMsg = err.code;
          });
      } else {
        this.errorMsg = "Please fill out all the fields!";
      }
    },
    isFormValid() {
      if (this.email !== null && this.password !== null) {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>
<style lang="scss" scoped >

.noAcc{
  display: flex;
  flex-direction: column;

  p{
    text-align: center;
  }
}
.google-button {
  max-height: 50px;
}
</style>
