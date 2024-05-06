<template>
  <form name="login-form" class="login-form">
    <div class="form-group">
      <label for="username">Username: </label>
      <input type="text" id="username" v-model="input.username" class="form-control" />
    </div>
    <div class="form-group">
      <label for="password">Password: </label>
      <input type="password" id="password" v-model="input.password" class="form-control" />
    </div>
    <button class="btn btn-primary btn-block" type="submit" v-on:click.prevent="login()">
      Login
    </button>
    <button @click="$router.push('/register')" class="btn btn-link btn-block">
      Register
    </button>
  </form>
  <h3 class="output">{{ output }}</h3>
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
        axios.post('http://localhost:8000/api/login', {
          username: this.input.username,
          password: this.input.password
        }).then(response => {
          if (response.data.authenticated) {
            this.$store.commit(`auth/${SET_AUTHENTICATION}`, true);
            this.$store.commit(`auth/${SET_USERNAME}`, this.input.username);
            this.output = "Authentication complete.";
            this.$router.push({ name: 'Home' });
          } else {
            this.output = "Authentication failed.";
          }
        }).catch(error => {
          const errorMessage = error.response && error.response.data && error.response.data.error
            ? error.response.data.error
            : error.message;
          if (error.response && error.response.status === 401) {
            this.output = "Wrong Username Or Password";
          } else {
            this.output = "Registration error: " + (error.response?.data?.error || error.message);
          }
          console.error("Registration error:", error);
          this.output = `login error: ${errorMessage}`;
          console.error("Login error:", error);
        });
      } else {
        this.output = "Username and password cannot be empty.";
      }
    },
  }
}
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100vh;
  align-items: center;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  /* subtle shadow for depth */
  padding: 2rem;
  border-radius: 0.5rem;
  /* rounded corners */
}

.form-group {
  margin-bottom: 1rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  /* slightly larger padding for better touch */
  font-size: 1rem;
  border: 1px solid #ced4da;
  /* updated to a lighter gray for subtlety */
  border-radius: 0.25rem;
  background-color: #f8f9fa;
  /* light background color */
}

.btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s;
  /* smooth transition */
}

.btn-primary {
  background-color: #007bff;
  /* primary blue */
  border: 1px solid #007bff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
  /* darker shade on hover */
  border-color: #0056b3;
}

.btn-link {
  color: #007bff;
  background: none;
  /* no background for a link-like button */
  border: none;
  padding: 0.5rem 0;
  /* reduced padding */
}

.btn-link:hover {
  color: #0056b3;
  text-decoration: underline;
  /* underline on hover for clarity */
}

.output {
  margin-top: 1rem;
  color: #dc3545;
  /* using a common error message color */
  font-size: 1rem;
}
</style>
