<template>
    <div class="home-container">
        <div class="left-section">
            <h1 id="site-name">[Your Site Name]</h1>
            <p>Engage with an interactive AI tutor to master new skills and concepts.</p>
        </div>
        <div class="divider"></div>
        <div class="right-section">
            <h1>Start Learning</h1>
            <div class="buttons">
                <router-link to="/login" class="btn btn-secondary">Log In</router-link>
                <router-link to="/register" class="btn btn-primary">Sign Up</router-link>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    name: 'HomeView'
}
</script>

<style scoped>
.right-section {
    background-color: #0056b3;
}

.left-section {
    background-color: sandybrown;
    padding: 100px;

}

.home-container {
    display: flex;
    height: 100vh;
    overflow: hidden;
}

.left-section,
.right-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}


.buttons {
    display: flex;
    flex-direction: row;
    gap: 10px;
}
.left-section p{
    margin-top: 100px;
    font-size: large;
}
.btn {
    margin-top: 40px;
    padding: 10px 25px;
    border: none;
    color: white;
    border-radius: 5px;
    text-decoration: none;
    font-size: 1em;
    transition: background-color 0.3s;
}

.btn-primary {
    background-color: #0077b6;
}

.btn-primary:hover {
    background-color: #0056b3;
}

.btn-secondary {
    background-color: #4d908e;
}

.btn-secondary:hover {
    background-color: #40798c;
}
</style>
