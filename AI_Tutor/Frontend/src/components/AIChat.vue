<template>
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
            axios.post('/api/chat', payload)
                .then(response => {
                    this.aiResponse = response.data.response;
                })
                .catch(error => {
                    console.error("Error communicating with the AI:", error);
                    this.aiResponse = 'Sorry, something went wrong.';
                });
        },
    },
};
</script>