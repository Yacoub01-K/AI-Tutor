<template>
  <div class="editor-container">
    <div ref="editorContainer" style="height: 300px;"></div>
    <button @click="runCode">Run Code</button>
    <div v-if="output" class="output-container">
      Output: <pre>{{ output }}</pre>
    </div>
  </div>
</template>

<script>
import * as monaco from 'monaco-editor';
import axios from 'axios';

export default {
  name: 'CodeEditor',
  data() {
    return {
      editor: null,
      output: '',
    };
  },
  mounted() {
    this.editor = monaco.editor.create(this.$refs.editorContainer, {
      value: `function hello() {\n  console.log("Hello, world!");\n}`,
      language: 'javascript',
      theme: 'vs-dark'
    });
  },
  methods: {
    runCode() {
      const code = this.editor.getValue();
      axios.post('http://localhost:8000/api/execute', { code })
        .then(response => {
          this.output = response.data.output;
        })
        .catch(error => {
          console.error('Error executing code:', error);
          this.output = 'Failed to execute code.';
        });
    }
  },
  beforeDestroy() {
    if (this.editor) {
      this.editor.dispose();
    }
  }
}
</script>

<style scoped>
.editor-container {
  margin: 20px;
}

.output-container {
  margin-top: 20px;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  padding: 10px;
}
</style>
