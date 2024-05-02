<template>
  <div>
    <Navbar />
    <CreateChatbot />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import CreateChatbot from '@/components/FrontPage.vue'; // Ensure correct file path

export default {
  name: 'HomeView',
  components: {
    Navbar,
    CreateChatbot
  }
};
</script>
