<template>
  <div>
    <h1>{{ lessonName }}</h1>
  </div>
  <div class="chat-container">
    <div class="messages-container">
      <div v-for="(message, index) in messages" :key="index" :class="`message ${message.sender}`">
        <p v-if="message.isHtml" v-html="message.content"></p>
        <p v-else>{{ message.content }}</p>
      </div>
    </div>
    <div class="input-container">
      <textarea v-model="userInput" placeholder="Ask me anything..." class="input-field"></textarea>
      <button @click="sendToAI" class="send-button">Send</button>
    </div>
    <button v-if="problemAvailable" @click="fetchAndEmitProblem">Get Problem</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userInput: '',
      messages: [],
      problemAvailable: false,
      problemDescription: '',
    };
  },
  computed:{
    lessonName() {
    return this.$store.state.lessonName;
    }
  },

  mounted() {
    this.loadMessages();
    if (this.$route.query.lessonName){
      this.lessonName = this.$route.query.lessonName;
      this.sendToAI(`Hi I would like to start a lesson on ${this.$route.params.topic} at ${this.$route.params.difficulty} level.`);
    }
  },

  
  methods: {
    
    sendToAI(input='') {
      const payload = { userInput: this.userInput };
      const message = input || this.userInput; 
      this.messages.push({ content: this.userInput, sender: 'user' });
      this.userInput = '';
      axios.post('http://localhost:8000/api/chat', payload)
        .then(response => {
          this.messages.push({
            content: response.data.response,
            sender: 'ai',
            isHtml: true
          });
          this.problemAvailable = response.data.problemAvailable;
          this.problemDescription = response.data.problemDescription;
          this.saveMessages();  // Save messages after response
        })
        .catch(error => {
          this.messages.push({
            content: `Error: ${error.response?.data.error || "Unable to connect"}`,
            sender: 'ai'
          });
        });
    },
    saveMessages() {
      localStorage.setItem('chatMessages', JSON.stringify(this.messages));
    },
    loadMessages() {
      const savedMessages = localStorage.getItem('chatMessages');
      if (savedMessages) {
        this.messages = JSON.parse(savedMessages);
      }
    },
    extractTopic(userInput) {
      const topics = new Set(['python', 'javascript', 'java', 'data structures', 'algorithms']);
      const words = new Set(userInput.toLowerCase().split(/\s+/));
      const foundTopics = [...topics].filter(topic => words.has(topic));
      return foundTopics.length > 0 ? foundTopics[0] : 'general programming';
    },
    assessDifficulty(userInput) {
      if (userInput.toLowerCase().includes('beginner')) {
        return 'beginner';
      } else if (userInput.toLowerCase().includes('intermediate')) {
        return 'intermediate';
      } else if (userInput.toLowerCase().includes('advanced')) {
        return 'advanced';
      }
      return 'beginner';
    },
    fetchAndEmitProblem() {
      const topic = this.extractTopic(this.userInput);
      const difficulty = this.assessDifficulty(this.userInput);
      console.log(difficulty);
      console.log(topic);
      axios.post('http://localhost:8000/api/get_problem', { topic, difficulty })
        .then(response => {
          this.problemDescription = response.data.problem;
          this.$store.dispatch('updateProblemDescription', this.problemDescription);
          this.$router.push({ name: 'Class' }); // Make sure this route name matches your Vue Router settings
        })
        .catch(error => {
          console.error('Error fetching problem:', error);
          this.messages.push({ content: "Failed to fetch problem.", sender: 'system' });
        });
    },
    getLessonName(description) {
      this.lessonName = description;

    }

  }
}
</script>


<style scoped>
.chat-container {
  width: 100%;
  max-width: 800px;
  margin: auto;
  background: #333; /* Darker background */
  border: 1px solid #444; /* Darker border */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Stronger shadow for depth */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 500px;
}

.messages-container {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 20px;
  background: #222;
  border: 1px solid #333; 
  border-radius: 4px;
  padding: 10px;
}

.message {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.message.user {
  background-color: #1a8cff; /* Bright blue for user messages */
  align-self: flex-end;
  max-width: 100%;
}

.message.ai {
  background-color: orange; /* Purple for AI messages */
  align-self: flex-start;
  max-width: 100%;
}

.input-container {
  display: flex;
  align-items: center;
}

.input-field {
  flex: 1;
  padding: 10px;
  border: 1px solid #555; /* Darker border for input */
  border-radius: 4px;
  outline: none;
  font-size: 16px;
  background: #222; /* Dark input field */
  color: #ddd; /* Light text color for readability */
}

.send-button {
  padding: 10px 20px;
  border: none;
  background-color: #5cb85c; /* Green for send button */
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

.send-button:hover {
  background-color: #4cae4c; /* Darker green on hover */
}
</style>


