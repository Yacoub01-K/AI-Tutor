<template>
  <div class="container">
    <div class="left-column">
      <div class="ai-chat">
        <h3>AI Chat</h3>
        <AIChat @problemDescriptionSend="handleProblemDescription"/>
      </div>
      <div class="problem-description">
        <h3>Problem Description</h3>
        <p>{{ problemDescription }}</p>
      </div>
    </div>
    <div class="right-column">
      <div class="code-editor">
        <h3>Code Editor</h3>
        <!-- Language Selector -->
        <select v-model="currentLanguage" @change="changeLanguage">
          <option v-for="lang in languages" :key="lang.value" :value="lang.value">{{ lang.text }}</option>
        </select>
        <div id="editor" style="height: 300px;"></div>
      </div>
      <button @click="executeCode">Run Code</button>
      <div class="console-output">
        <h3>Console Output</h3>
        <div v-text="output"></div>
      </div>
    </div>
  </div>
</template>

<script>
import loader from '@monaco-editor/loader';
import AIChat from '@/components/AIChat.vue'
import axios from 'axios'

export default {
  name: 'MonacoEditor',
  components: {
    AIChat,
  },

  data() {
    return {
      output: '',
      isLoading: false,
      editorInstance: null,
      currentLanguage: 'python',
      languages: [
        { text: 'Python', value: 'python' },
        { text: 'JavaScript', value: 'javascript' },
        { text: 'HTML', value: 'html' },
        { text: 'CSS', value: 'css' },
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
    if (this.$route.query.problem) {
    this.problemDescription = this.$route.query.problem;
  }

    loader.init().then(monaco => {
      this.editorInstance = monaco.editor.create(document.getElementById('editor'), {
        language: this.currentLanguage,
        theme: 'vs-dark',
        value: 'type your code here...',
      });
    });
  },
  methods: {
    handleProblemDescription(description) {
      console.log("The dis:"+description);
      this.problemDescription = description;
    },
    executeCode() {
      const code = this.editorInstance.getValue();
      this.isLoading = true;
      axios.post('http://localhost:8000/api/execute', { code, language: this.currentLanguage })
        .then(response => {
          this.output = response.data.output;
        })
        .catch(error => {
          this.output = `Error: ${error.response.data.message || error.message}`;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    changeLanguage() {
      if (this.editorInstance) {
        const model = this.editorInstance.getModel();
        loader.init().then(monaco => {
          monaco.editor.setModelLanguage(model, this.currentLanguage);
        });
      }
    }
  }
}
</script>


<style scoped>
.container {
  display: flex;
  height: 100vh;
}

.left-column,
.right-column {
  width: 50%;
  padding: 20px;
}

.ai-chat,
.problem-description {
  margin-bottom: 20px;
}

.chat-messages,
.console-output {
  height: 150px;
  border: 1px solid #ccc;
  margin-top: 10px;
  padding: 10px;
  overflow-y: auto;
}

textarea {
  width: 100%;
  height: 300px;
}
</style>
