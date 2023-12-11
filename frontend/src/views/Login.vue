<template>
  <main class="login-page">
    
    <h1 class="text">Login</h1>

    <form @submit.prevent="loginUser" class="login-form">
      <label for="email">Email:</label>
      <input type="text" id="email" v-model="email" required>

      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required>

      <button type="submit">Login</button>
    </form>

  </main>
</template>

  
<script setup>
import { ref } from 'vue'
import { API_BASE_URL } from '../config'

const email = ref('')
const password = ref('')

const loginUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/jwt/login`, {
      method: "POST",
      headers: {
          "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
          username: email.value,
          password: password.value,
          grant_type: '',
          scope: '',
          client_id: '',
          client_secret: '',
      }),
      credentials: "include",
    });

    if(!response.ok) {
      throw new Error('Login failed! Check your email and password.');
    }

    window.location.href = "/chat"
  } catch (error) {
    console.error('Error during login:', error.message);
  }
}

</script>

<style scoped>

.text {
  padding: 10px;
}

.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.login-form {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #fff;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: var(--primary);
  color: #fff;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>