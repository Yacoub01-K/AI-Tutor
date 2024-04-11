<template>
    <div class="container">
      <!-- Left Column for AI and Problem Description -->
      <div class="left-column">
        <!-- AI Chat Area -->
        <div class="ai-chat">
          <h3>AI Chat</h3>
          <!-- Placeholder for chat messages -->
          <div class="chat-messages">
            <p>Message from AI...</p>
          </div>
          <!-- Input area for asking questions -->
          <input type="text" placeholder="Ask a question...">
          <button>Send</button>
        </div>
        <!-- Problem Description Area -->
        <div class="problem-description">
          <h3>Problem Description</h3>
          <p>This is where the AI-generated coding problem will be displayed.</p>
        </div>
      </div>
  
      <!-- Right Column for Code Editor and Console -->
      <div class="right-column">
        <!-- Code Editor Area -->
        <div class="code-editor">
          <h3>Code Editor</h3>
          <textarea placeholder="Write your code here..."></textarea>
        </div>
        <!-- Console Output Area -->
        <div class="console-output">
          <h3>Console Output</h3>
          <div>Output from code execution will appear here.</div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .container {
    display: flex;
    height: 100vh;
  }
  
  .left-column, .right-column {
    width: 50%;
    padding: 20px;
  }
  
  .ai-chat, .problem-description {
    margin-bottom: 20px;
  }
  
  .chat-messages, .console-output {
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
  
  
<script>
 /**
  * add nav bar here.
  */
</script>
  