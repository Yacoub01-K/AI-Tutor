<template>
    <nav class="navbar">
        <div class="logo-container">
            <img src="@/assets/logo2.png" alt="Your Logo" class="navbar-logo">
        </div>
        <div class="navbar-menu">
            <router-link to="/account" class="navbar-item">Account</router-link>
            <router-link to="/settings" class="navbar-item"> 
                <img src="@/assets/icons8-settings-48.png" alt="setting" class = "settings">
            </router-link>
            <button @click="logout()" class="navbar-item">Logout</button>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'Navbar',
    methods: {
        logout() {
            // Perform logout logic, e.g., clear the user token, update Vuex state
            this.$store.commit('logout');
            this.$router.replace('/');
        }
    }
}
</script>

<style scoped>
.navbar {
    display: flex;
    justify-content: space-between;
    background-color: #f8f9fa;
    padding: 1rem;
}

.navbar-brand {
    font-weight: bold;
}

.navbar-menu {
    display: flex;
    align-items: center;
}

.navbar-item {
    margin-left: 1rem;
    cursor: pointer;
    text-decoration: none;
    color: #333;
}

.navbar-item:hover {
    text-decoration: underline;
}

.logo-container {
    display: flex;
    align-items: center;
}

.navbar-logo {
    height: 50px;
    width: auto;
    margin-right: 20px;
}
.settings {
    transform: scale(0.5); 
}
</style>