<template>
    <div>
        <h1>AI Tutor</h1>
    </div>
    <div>
        <textarea v-model="userInput" placeholder="Ask me anything..."></textarea>
        <button @click="sendToAI">Ask AI</button>
        <div v-if="aiResponse">{{ aiResponse }}</div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            userInput: '',
            aiResponse: '',
        };
    },
    methods: {
        sendToAI() {
            const payload = {
                userInput: this.userInput,
            };
            axios.post('http://localhost:8000/api/chat', payload)
                .then(response => {
                    this.aiResponse = response.data;
                })
                .catch(error => {
                    console.error("Full error response:", error.response);
                    const errorMessage = error.response && error.response.data && error.response.data.error
                        ? error.response.data.error
                        : error.message;
                    this.aiResponse = `Sorry, something went wrong: ${errorMessage}`;
                });
        },
    },
};
</script>
