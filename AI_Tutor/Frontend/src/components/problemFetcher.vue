<template>
    <div v-if="problemAvailable">
      <button @click="transferData">Get Problem</button>
      <div v-if="problemDescription">{{ problemDescription }}</div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['problemAvailable', 'dataToTransfer'],
    data() {
      return {
        problemDescription: ''
      };
    },
    methods: {
      transferData() {
        if (this.problemAvailable) {
          this.$emit('dataTransferred', this.dataToTransfer);
          this.problemDescription = this.dataToTransfer;
          this.$router.push({ name: 'Class' });
        }
      }
    }
  }
  </script>
  