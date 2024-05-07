<template>
  <div class="container">
    <div class="left-column">
      <div class="ai-chat">
        <AIChat @problemDescriptionSend="handleProblemDescription" />
      </div>
      <div class="problem-description">
        <h3>Problem Description</h3>
        <p>{{ problemDescription }}</p>
      </div>
    </div>
    <div class="right-column">
      <div class="code-editor">
        <select v-model="currentLanguage" @change="changeLanguage">
          <option v-for="lang in languages" :key="lang.value" :value="lang.value">{{ lang.text }}</option>
        </select>
        <div id="editor" style="height: 500px;"></div>
        <button @click="executeCode" :disabled="isLoading">Run Code</button>
        <div v-if="isLoading">Running...</div>
      </div>
      <div class="console-output">
        <h3>Console Output</h3>
        <pre>{{ output }}</pre>
        <div v-if="error" class="error">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import ace from 'ace-builds';
import 'ace-builds/src-noconflict/theme-tomorrow_night';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-html';
import 'ace-builds/src-noconflict/mode-css';
import 'ace-builds/src-noconflict/mode-typescript';
import 'ace-builds/src-noconflict/mode-json';
import AIChat from '@/components/AIChat.vue';
import axios from 'axios';

export default {
  name: 'CodeEditor',
  components: {
    AIChat,
  },
  data() {
    return {
      problemDescription: '',
      output: '',
      error: '',
      isLoading: false,
      editor: null,
      currentLanguage: 'python',
      languages: [
        { text: 'Python', value: 'python' },
        { text: 'JavaScript', value: 'javascript' },
        { text: 'Java', value: 'java' },
        { text: 'TypeScript', value: 'typescript' },
        { text: 'JSON', value: 'json' },
      ],
    };
  },
  computed: {
    problemDescription() {
      return this.$store.state.problemDescription;
    }
  },
  mounted() {
    this.initializeAce();
    if (this.$route.query.problem) {
    this.problemDescription = this.$route.query.problem;
    }
  },
  
  methods: {
    handleProblemDescription(description) {
      console.log("The dis:" + description);
      this.problemDescription = description;
    },
    initializeAce() {
      ace.config.set('basePath', '/path/to/ace'); // Correct path needed
      this.editor = ace.edit("editor");
      this.editor.setTheme("ace/theme/tomorrow_night");
      this.editor.session.setMode(`ace/mode/${this.currentLanguage}`);
    },
    changeLanguage() {
      this.editor.session.setMode(`ace/mode/${this.currentLanguage}`);
    },
    executeCode() {
      this.isLoading = true;
      const code = this.editor.getValue();
      axios.post('http://localhost:8000/api/execute', {
        code: code,
        language: this.currentLanguage
      }, { timeout: 30000})
      
      .then(response => {
        console.log(response.data.output);
        this.output = response.data.output;
        this.isLoading = false;
      })
      .catch(error => {
        this.error = error.response?.data?.error || "Execution Error: " + error.message;
        this.isLoading = false;
      });
    }
  }
}
</script>

<style scoped>
.ai-chat {
    width: 90%;  /* Reduce width */
    height: auto; /* Set a fixed height */
    padding: 10px; /* Adjust padding to reduce size */
    margin-bottom: 20px; /* Keeps existing bottom margin */
    margin: 10px 0;
}
.right-column {
    width: 60%; /* Increase the width of the right column */
}

.container {
  display: flex;
  height: 100vh;
}
.error {
  color: red;
}
.left-column, .right-column {
  width: 50%;
  padding: 20px;
}
.ai-chat, .problem-description {
  margin-bottom: 20px;
}
.console-output {
  height: 150px;
  border: 1px solid #ccc;
  margin-top: 10px;
  padding: 10px;
  overflow-y: auto;
}
.left-column {
    flex: 1;  /* Takes less space */
}
.ai-chat h3, .ai-chat p {
    font-size: smaller; /* Reduces the font size of headings and paragraphs */
}
</style>
