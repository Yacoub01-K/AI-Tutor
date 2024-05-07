<template>
    <div class="container">
        <div v-for="lesson in lessons" :key="lesson.name" class="lesson-button" @click="goToLesson(lesson)">
            {{ lesson.name }} - {{ lesson.topic }}
            <button class="menu-button" @click="toggleMenu(lesson.id)">⋮</button>
            <div v-if="lesson.showMenu" class="dropdown-menu" @click.stop>
                <ul>
                    <li @click="pinLesson(lesson.id)">Pin Lesson</li>
                    <li @click="deleteLesson(lesson.id)">Delete Lesson</li>
                </ul>
            </div>
        </div>
        <button @click="showModal" class="plus-button">+</button>

        <div v-if="modalVisible" class="modal-overlay">
            <div class="modal-content">
                <span class="close" role="button" aria-label="Close" @click="closeModal">&times;</span>
                <h2>Create New Lesson</h2>
                <form @submit.prevent="submitLesson">
                    <div class="form-group">
                        <label for="lessonName">Class/Lesson Name:</label>
                        <input type="text" id="lessonName" v-model="lessonName" required>
                    </div>
                    <div class="form-group">
                        <label for="lessonTopic">Lesson Topic:</label>
                        <input type="text" id="lessonTopic" v-model="lessonTopic" required>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="submit-button">Create</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CreateChatbot',
    data() {
        return {
            modalVisible: false,
            lessonName: '',
            lessonTopic: '',
            lessons: []
        };
    },
    methods: {
        showModal() {
            this.modalVisible = true;
        },
        closeModal() {
            this.modalVisible = false;
        },
        submitLesson() {
            if (this.lessonName && this.lessonTopic) {
                this.lessons.push({ name: this.lessonName, topic: this.lessonTopic });
                this.lessonName = '';
                this.lessonTopic = '';
                this.closeModal();
            }
        },

        toggleMenu(lessonId) {
            this.lessons = this.lessons.map(lesson =>
                lesson.id === lessonId ? { ...lesson, showMenu: !lesson.showMenu } : lesson
            );
        },
        pinLesson(lessonId) {
            // Implement pinning logic
            console.log('Pinning lesson:', lessonId);
            this.closeMenus();
        },
        deleteLesson(lessonId) {
            // Implement delete logic
            console.log('Deleting lesson:', lessonId);
            this.lessons = this.lessons.filter(lesson => lesson.id !== lessonId);
            this.closeMenus();
        },
        closeMenus() {
            this.lessons = this.lessons.map(lesson => ({ ...lesson, showMenu: false }));
        }
    }
};
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 125px;
    /* Adjust this value so that it's slightly more than the navbar height */
    width: 100%;
    /* Ensures the container uses the full width */
}

.lesson-button {
    display: flex;
    align-items: center;
    justify-content: space-between;
    text-align: center;
    width: 100%;
    max-width: 500px;
    height: 50px;
    margin: 10px 0;
    padding: 10px 20px;
    background-color: #104DA5;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.lesson-button:hover,
.plus-button:hover {
    opacity: 0.9;
}

.plus-button {
    margin-top: auto;
    /* Ensures that the button stays at the bottom */
    background-color: #4CAF50;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    font-size: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
}

.modal-content {
    background: #FFF;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    width: 100%;
    max-width: 500px;
    transition: transform 0.3s ease-out;
}

.form-group label {
    display: block;
    font-weight: 600;
    color: #333;
}

.form-group input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}

.submit-button {
    margin-top: 15px;
    background-color: #4CAF50;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    width: 100%;
    color: white;
    border: none;
}

.dropdown-menu {
    position: absolute;
    right: 20px;
    top: 50px;
    /* Adjusts dropdown position */
    z-index: 10;
    /* Ensures dropdown is above other elements */
}

.menu-button {
    font-size: 24px;
    color: #333;
}

.dropdown-menu li:hover {
    background-color: #E2E4E6;
}
.lesson-button:focus, .plus-button:focus {
    box-shadow: 0 0 0 3px rgba(255,255,255,0.5);
}

.close:hover {
    color: #666; /* Darker shade on hover for visual feedback */
    cursor:pointer;
}
</style>
