<template>
    <div class="chat-container">
      <div class="messages-container">
        <!-- Render messages here -->
        <div v-for="(message, index) in messages" :key="index" :class="`message ${message.sender}`">
          <p>{{ message.content }}</p>
        </div>
      </div>
      <div class="input-container">
        <textarea v-model="userInput" placeholder="Ask me anything..." class="input-field"></textarea>
        <button @click="sendToAI" class="send-button">Send</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
      data() {
          return {
              userInput: '',
              aiResponse: '',
              messages: [],
          };
      },
      methods: {
          sendToAI() {
              const payload = { userInput: this.userInput };
              this.messages.push({ content: this.userInput, sender: 'user' });
              axios.post('http://localhost:8080/api/chat', payload)
                  .then(response => {
                      this.messages.push({ content: response.data, sender: 'ai' });
                      this.userInput = ''; // Clear input after sending
                  })
                  .catch(error => {
                      const errorMessage = error.response && error.response.data && error.response.data.error
                          ? error.response.data.error
                          : 'Unable to connect.';
                      this.messages.push({ content: `Error: ${errorMessage}`, sender: 'ai' });
                  });
          },
      },
  };
  </script>
  
  <style scoped>
  .chat-container {
    width: 100%;
    max-width: 600px;
    margin: auto;
    background: #f4f5f7;
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 8px;
  }
  
  .messages-container {
    height: 300px;
    overflow-y: auto;
    margin-bottom: 20px;
    padding: 10px;
    background: white;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .message {
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 4px;
  }
  
  .message.user {
    background-color: #b2dffb;
    text-align: right;
  }
  
  .message.ai {
    background-color: #e5e5e5;
    text-align: left;
  }
  
  .input-container {
    display: flex;
  }
  
  .input-field {
    flex: 1;
    margin-right: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .send-button {
    padding: 10px 20px;
    border: none;
    background-color: #007BFF;
    color: white;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .send-button:hover {
    background-color: #0056b3;
  }
  </style>
  