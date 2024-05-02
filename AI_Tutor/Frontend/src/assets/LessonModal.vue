<template>
    <div v-if="visible" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <form @submit.prevent="submitLesson">
          <label for="lessonName">Name the class/lesson:</label>
          <input type="text" id="lessonName" v-model="lessonName" required>
  
          <label for="lessonTopic">Lesson topic:</label>
          <input type="text" id="lessonTopic" v-model="lessonTopic" required>
  
          <button type="submit">Done</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        lessonName: '',
        lessonTopic: '',
        visible: false
      };
    },
    methods: {
      closeModal() {
        this.visible = false;
      },
      submitLesson() {
        this.$emit('addLesson', { name: this.lessonName, topic: this.lessonTopic });
        this.lessonName = '';
        this.lessonTopic = '';
        this.closeModal();
      }
    }
  };
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    width: 300px;
  }
  
  .close {
    float: right;
    cursor: pointer;
  }
  </style>
  