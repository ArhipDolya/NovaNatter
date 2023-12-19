<template>
  <main class="login-page">
    <h1 class="text">Login</h1>

    <form @submit.prevent="loginUser" class="login-form">
      <label for="email">Email:</label>
      <input type="text" id="email" v-model="email" required>

      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required>

      <div class="remember-me">
        <label for="rememberMe">Remember me:</label>  
        <input type="checkbox" id="rememberMe" v-model="rememberMe">
      </div>

      <button type="submit">Login</button>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { API_BASE_URL } from '../config'

const email = ref<string>('')
const password = ref<string>('')
const rememberMe = ref<boolean>(false)

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
          rememberMe: rememberMe.value.toString(),
      }),
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error('Login failed! Check your email and password.');
    }

    window.location.href = '/chat';
  } catch (error) {
    console.error('Error during login:', error.message);
  }
};
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

.remember-me {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.remember-me input {
  margin-right: 200px;
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
