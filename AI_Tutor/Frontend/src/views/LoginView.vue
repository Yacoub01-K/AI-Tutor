<template>
  <form name="login-form">
    <div class="mb-3">
      <label for="username">Username: </label>
      <input type="text" id="username" v-model="input.username" />
    </div>
    <div class="mb-3">
      <label for="password">Password: </label>
      <input type="password" id="password" v-model="input.password" />
    </div>
    <button class="btn btn-outline-dark" type="submit" v-on:click.prevent="login()">
      Login
    </button>
  </form>
  <h3>Output: {{ this.output }}</h3>

</template>

<script>
import { SET_AUTHENTICATION, SET_USERNAME } from "../store/storeconstants";
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      input: {
        username: "",
        password: ""
      },
      output: "",
    };
  },
  methods: {
    login() {
      if (this.input.username !== "" && this.input.password !== "") {
        axios.post('http://localhost:8080/api/login', {
          username: this.input.username,
          password: this.input.password
        }).then(response => {
          if (response.data.authenticated) {
            this.$store.commit(`auth/${SET_AUTHENTICATION}`, true);
            this.$store.commit(`auth/${SET_USERNAME}`, this.input.username);
            this.output = "Authentication complete.";
            console.log("working")
            this.$router.push({ name: 'Home' });
          } else {
            this.output = "Authentication failed.";
          }
        }).catch(error => {
          const errorMessage = error.response && error.response.data && error.response.data.error
                        ? error.response.data.error
                        : error.message;
          this.output = `login error: ${errorMessage}`;
          console.error("Login error:", error);
        });
      } else {
        this.output = "Username and password cannot be empty.";
      }
    },

  },
}
</script>