<template>
  <main class="home-page">
    <template v-if="state.isLoggedIn !== null">
      <h1 v-if="state.isLoggedIn">Welcome, User!</h1>
      <h1 v-else>Home</h1>
    </template>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { API_BASE_URL } from '../config'
import axios from 'axios'

interface HomeState {
  isLoggedIn: boolean | null;
}

const state = ref<HomeState>({
  isLoggedIn: null,
})

const checkAuthentication = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/auth/user/status`, {
      withCredentials: true, // Use withCredentials instead of credentials
    })

    if (response.status === 200) {
      state.value.isLoggedIn = true;
    } else {
      state.value.isLoggedIn = false;
    }

  } catch (error) {
    console.error('Error checking authentication:', error);
    state.value.isLoggedIn = false;
  }
}

onMounted(() => {
  checkAuthentication();
})
</script>