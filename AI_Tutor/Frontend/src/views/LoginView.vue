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
      // Check that both username and password are not empty
      if (this.input.username !== "" && this.input.password !== "") {
        this.$store.commit(`auth/${SET_AUTHENTICATION}`, true);
        this.$store.commit(`auth/${SET_USERNAME}`, this.input.username);
        this.output = "Authentication complete.";
        this.$router.push({ name: 'AI' });
      } else {
        // No need to commit a false authentication here if you handle the output message properly
        this.output = "Username and password cannot be empty.";
      }
    },
  },
}
  </script>