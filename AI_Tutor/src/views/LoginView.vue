<template>
    <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="login">
            <div>
                <label for="username">Username:</label>
                <input id="username" v-model="credentials.username" type="text" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input id="password" v-model="credentials.password" type="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
export default {
name: 'LoginView',
    data() {
    return {
        credentials: {
            username: '',
            password: '',
        },
    };
},
methods: {
        async login() {
        console.log('Attempting to log in with', this.credentials);
        // Assuming you have an authentication method to validate credentials
        const isAuthenticated = await authenticateUser(this.credentials);
        if (isAuthenticated) {
            this.$router.push('/home'); // Redirect to HomeView after successful login
        } else {
            // Handle login failure (e.g., display an error message)
        }
    }
},
}
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: auto;
    padding: 20px;
}
</style>