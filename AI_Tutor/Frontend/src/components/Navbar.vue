<template>
    <nav class="navbar">
        <div class="logo-container">
            <img src="@/assets/logo2.png" alt="Logo" class="navbar-logo">
        </div>
        <div class="navbar-menu">
            <div class="navbar-dropdown">
                <button @click="toggleDropdown" class="navbar-item dropdown-toggle">
                    <div class="profile-info">
                        <img alt="Profile" class="profile-icon">
                        <span class="profile-name">[USERNAME]</span>
                    </div>
                </button>
                <div v-if="showDropdown" class="dropdown-menu">
                    <div class="dropdown-item">Email: {{ userEmail }}</div>
                    <button class="dropdown-item my-plan">My Plan</button>
                    <button @click="logout()" class="dropdown-item logout-button">Logout</button>
                </div>
            </div>
            <router-link to="/settings" class="navbar-item">
                <img src="@/assets/icons8-settings-48.png" alt="Settings" class="settings-icon">
            </router-link>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'Navbar',
    data() {
        return {
            showDropdown: false
        };
    },
    methods: {
        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
        },
        logout() {
            // Perform logout logic, e.g., clear the user token, update Vuex state
            this.$store.commit('logout');
            this.$router.replace('/');
        }
    }
}
</script>


<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body, html {
    width: 100%;
    height: 100%;
    font-family: 'Arial', sans-serif;
    background-color: #f4f7fa;
    color: #333;
}
.navbar-dropdown {
    position: relative;
}

.dropdown-toggle {
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    font-size: 16px;
    display: flex;
    align-items: center;
}

.profile-abbreviation {
    background: #1a73e8;
    color: #ffffff;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 8px;
    font-weight: bold;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background-color: #ffffff;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1001;
    display: none;
    min-width: 250px; /* Minimum width of the dropdown */
    max-width: 400px; /* Maximum width of the dropdown */
    width: auto; /* Width auto adjusts based on content up to max width */
}

.navbar-dropdown:hover .dropdown-menu {
    display: block;
}

.dropdown-item {
    padding: 8px 16px;
    text-decoration: none;
    display: block;
    color: #333;
    transition: background-color 0.3s;
}

.dropdown-item:hover {
    background-color: #f9f9f9;
}
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #89ABE3FF;
    width: 100vw;
    height: 80px;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.profile-abbreviation{
    margin-right: 200px;
}

.logo-container {
    padding-left: 20px;
}

.navbar-logo {
    height: 40px;
}

.navbar-menu {
    padding-right: 20px;
    display: flex;
    align-items: center;
}

.navbar-item {
    color: #FFFFFF;
    margin-left: 20px;
    font-size: 16px;
    text-decoration: none;
}

.navbar-item:hover {
    text-decoration: underline;
    color: #DDEFFF;
}

.logout-button {
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    font-size: 16px;
}
.my-plan{
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    font-size: 16px;  
}

.logout-button:hover {
    text-decoration: underline;
}
.my-plan:hover{
    text-decoration: underline;
}
</style>
