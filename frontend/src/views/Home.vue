<template>
  <main class="home-page">
    <h1 v-if="isLoggedIn">Welcome, User!</h1>
    <h1 v-else>Home</h1>
  </main>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { API_BASE_URL } from '../config'

const isLoggedIn = ref(false);

const checkAuthentication = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/user/status`, {
      method: "GET",
      credentials: "include",
    })

    if (response.ok) {
      isLoggedIn.value = true;
    } else {
      isLoggedIn.value = false;
    }

  } catch (error) {
    console.error('Error checking authentication:', error);
  }
}

onMounted(() => {
  checkAuthentication();
})

</script>
