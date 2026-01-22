<template>
  <body class="reset-password">
    <Modal
      v-if="modalActive"
      :modalMessage="modalMessage"
      v-on:close-modal="closeModal"
    />
    <div class="form-wrap">
      <form class="reset">
        <h2>Reset Password</h2>
        <p class="login-register">
          Forgot your password? enter your email to reset it
        </p>
        <div class="inputs">
          <div class="input">
            <input type="text" placeholder="Email" v-model="email" />
            <email class="icon" />
          </div>
        </div>
        <button @click.prevent="resetPassword">Reset</button>
      </form>
      <div class="background"></div>
    </div>
  </body>
</template>

<script>
import email from "../assets/Icons/envelope-regular.svg";
import Modal from "../components/Modal";
import firebase from "firebase/app";
import "firebase/auth";

export default {
  name: "ForgotPassword",

  data() {
    return {
      email: null,
      modalActive: null,
      modalMessage: "",
      loading: null,
    };
  },

  components: {
    email,
    Modal,
  },

  methods: {
    resetPassword() {
      this.loading = true;
      firebase
        .auth()
        .sendPasswordResetEmail(this.email)
        .then(() => {
          this.modalMessage =
            "If your account exists, you will recieve a email";
          this.loading = false;
          this.modalActive = true;
        })
        .catch((err) => {
          this.modalMessage = err.message;
          this.loading = false;
          this.modalActive = true;
        });
    },

    closeModal() {
      this.modalActive = !this.modalActive;
      this.email = "";
    },
  },
};
</script>

<style lang="scss" scoped>
.reset-password {
  width: 100%;
  display: flex;
  flex-direction: column;
  .form-wrap {
    .inputs {
      display: flex;
      flex-direction: column;
      text-align: center;
      padding: 10px;

      input {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid black;
      }

      
    }
   
    .reset {
        display: flex;
        flex-direction: column;
      h2 {
        margin-bottom: 8px;
        text-align: center;
      }

      p {
        text-align: center;
        margin-bottom: 32px;
      }
       button {
        background-color: rgb(72, 143, 239);
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        width: 30%;
        margin-left: 35%;
        margin-top: 3%;
      }
    }
  }
}
</style>