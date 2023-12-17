<template>
  <div class="profile-container">
    <h1>Profile</h1>
    <div v-if="username" class="username-info">
      <img src="\src\assets\user-avatar.png" alt="User Avatar" class="user-avatar" />
      <span class="username-text">Username: {{ username }}</span>
    </div>

  </div>
</template>
  
<script lang="ts">
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../config';
import axios from 'axios'

export default {
  setup() {
    const username = ref<string | null>('');

    const getUserInfo = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/user/me`, {
          credentials: 'include',
        });

        if (response.ok) {
          const userInfo = await response.json();
          username.value = userInfo.username;
        } else {
          console.error('Failed to fetch user info');
        }
      } catch (error) {
        console.error('Error during fetch:', error.message);
      }
    };

    onMounted(getUserInfo);

    return {
      username,
    };
  },
};
</script>
  
<style scoped>
.profile-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
}

.username-info {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.user-avatar {
  width: 70px;
  height: 55px;
  border-radius: 50%;
  margin-right: 10px;
}

.username-text {
  font-size: 1.2rem;
}
</style>
  