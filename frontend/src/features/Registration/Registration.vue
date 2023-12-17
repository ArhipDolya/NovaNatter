<template>
  <main class="registration-page">
    <h1 class="text">Registration</h1>

    <form @submit.prevent="registerUser" class="registration-form">
      <label for="username">Username</label>
      <input type="text" id="username" v-model="username" required>

      <label for="email">Email</label>
      <input type="email" id="email" v-model="email" required>

      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" required>

      <button type="submit">Register</button>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { API_BASE_URL } from '../config';
import axios from 'axios'


const username = ref<string>('');
const email = ref<string>('');
const password = ref<string>('');

const registerUser = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      username: username.value,
      email: email.value,
      password: password.value,
    });

    if (!response.ok) {
      throw new Error('Registration failed! Try again!');
    }

    // If registration is successful, redirect to the login page
    window.location.href = "/login";
  } catch (error) {
    console.error('Error during registration:', error.message);
  }
};
</script>

<style scoped>

.text {
  padding: 10px;
}

.registration-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.registration-form {
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
  background-color: #4caf50;
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
