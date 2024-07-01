<template>
    <div class="register-container">
        <form name="register-form" class="register-form" @submit.prevent="register">
            <h3 v-if="output" class="output">{{ output }}</h3>
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="input.username" class="form-control"
                    placeholder="Enter your username" required />
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="input.email" class="form-control" placeholder="Enter your email"
                    required />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input :type="showPassword1 ? 'text' : 'password'" id="password" v-model="input.password"
                    class="form-control" placeholder="Create a password" required />
                <span @click="togglePasswordVisibility1" class="toggle-password">{{ showPassword1 ? '👁️' : '👁️‍🗨️' }}</span>
            </div>
            <div class="form-group">
                <label for="confirm-password">Confirm Password:</label>
                <input :type="showPassword2 ? 'text' : 'password'" id="confirm-password" v-model="input.confirmPassword"
                    class="form-control" placeholder="Confirm your password" required />
                <span @click="togglePasswordVisibility2" class="toggle-password">{{ showPassword2 ? '👁️' : '👁️‍🗨️' }}</span>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Register</button>
            <p style="padding: 15px 15px">Already have an account?</p>
            <button type="submit" class="btn btn-link btn-block" @click="login()">Login</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import { SET_AUTHENTICATION, SET_USERNAME } from "../store/storeconstants";

export default {
    name: 'RegisterView',
    data() {
        return {
            input: {
                username: "",
                email: "",
                password: "",
                confirmPassword: ""
            },
            showPassword1: false,
            showPassword2: false,
            output: ""
        };
    },
    methods: {
        async register() {
            if (this.input.password !== this.input.confirmPassword) {
                this.output = "Passwords do not match.";
                return;
            }

            try {
                const response = await axios.post('http://localhost:8000/api/add_user', {
                    username: this.input.username,
                    email: this.input.email,
                    password: this.input.password
                });
                console.log("Registration response:", response);
                this.output = "Registration successful.";
                this.$store.commit(`auth/${SET_AUTHENTICATION}`, true);
                this.$store.commit(`auth/${SET_USERNAME}`, this.input.username);
                this.$router.push({ name: 'Home' });
            } catch (error) {
                console.error("Registration error:", error);
                if (error.response) {
                    if (error.response.status === 409) {
                        const errorMsg = error.response.data.error;
                        if (errorMsg === 'Username already exists') {
                            this.output = "Username already exists.";
                        } else if (errorMsg === 'Email already exists') {
                            this.output = "Email already exists.";
                        } else {
                            this.output = "Username or email already exists.";
                        }
                    } else {
                        this.output = "Registration error: " + (error.response.data.error || error.message);
                    }
                } else {
                    this.output = "Registration error: " + error.message;
                }
            }
        },
        togglePasswordVisibility1() {
            this.showPassword1 = !this.showPassword1;
        },
        togglePasswordVisibility2() {
            this.showPassword2 = !this.showPassword2;
        },

        login(){
            this.$router.push({name: 'Login'});
        }
    }
}
</script>

<style scoped>
.register-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.register-form {
    max-width: 300px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100vh;
    align-items: center;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    padding: 2rem;
    border-radius: 0.5rem;
}

.form-group {
    margin-bottom: 1rem;
    position: relative;
}

.input-wrapper {
    display: flex;
    align-items: center;
    position: relative;
}

.form-control {
    width: 100%;
    padding-right: 30px;
    padding: 0.75rem;
    font-size: 1rem;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    background-color: #f8f9fa;
}

.toggle-password {
    cursor: pointer;
    position: absolute;
    right: 10px;
    padding: 10px;
}

.btn {
    display: block;
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    text-align: center;
    cursor: pointer;
    transition: background-color 0.3s, border-color 0.3s;
}

.btn-primary {
    background-color: #007bff;
    border: 1px solid #007bff;
    color: #fff;
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

.output {
    margin-top: 1rem;
    color: #dc3545;
    font-size: 1rem;
    font-size: bold;
    text-align: center;
    max-width: 300px;
    padding-bottom: 50px;
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


</style>
