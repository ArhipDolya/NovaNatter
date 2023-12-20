<template>
  <main class="login-page">
    <h1 class="text">Login</h1>

    <form @submit.prevent="loginUser" class="login-form">
      <label for="email">Email:</label>
      <input type="text" id="email" v-model="email" />
      <span v-if="formSubmitted && email && !isValidEmail" class="invalid-email">
        <svg fill="red" height="12" width="12" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-12c-.53 0-1 .47-1 1s.47 1 1 1 1-.47 1-1-.47-1-1-1zm-.5 4.5h1v3h-1v-3zm0 5h1v1h-1v-1z"/>
        </svg> Invalid email
      </span>

      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" />
      <span v-if="formSubmitted && password && !isPasswordValid" class="invalid-password">
        <svg fill="red" height="12" width="12" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path d="M0 0h24v24H0z" fill="none"/>
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
        </svg> Password too short
      </span>

      <div class="remember-me">
        <label for="rememberMe">Remember me:</label>
        <input type="checkbox" id="rememberMe" v-model="rememberMe" />
      </div>

      <button type="submit" @click="formSubmitted = true">Login</button>
    </form>
  </main>
</template>



<script setup lang="ts">
import { ref, computed } from 'vue'
import { API_BASE_URL } from '../config'
import { isValidEmailFormat, isValidPassword }from './utils'

const email = ref<string>('')
const password = ref<string>('')
const rememberMe = ref<boolean>(false)
const formSubmitted = ref<boolean>(false)


const isValidEmail = computed(() => isValidEmailFormat(email.value));
const isPasswordValid  = computed(() => isValidPassword(password.value));


const loginUser = async () => {

  if (!isValidEmail.value || !isPasswordValid.value) {
    console.error('Form has validation errors.');
    return;
  }

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

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 4px;
  display: inline-block;
}

.invalid-email, .invalid-password {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.invalid-email svg, .invalid-password svg {
  margin-right: 8px;
} 

</style>
