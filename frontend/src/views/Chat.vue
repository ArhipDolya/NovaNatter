<template>
  <div class="chat-container">
    <h1>WebSocket Chat</h1>
    <h2>Your name: <span>{{ username }}</span></h2>
    <form @submit.prevent="sendMessage" class="message-form">
      <input v-model="messageText" type="text" autocomplete="off" class="message-input" />
      <button type="submit" class="send-button">Send</button>
    </form>
    <ul class="message-list">
      <li v-for="(message, index) in messages" :key="index" class="message">{{ message.content }}</li>
    </ul>
  </div>
</template>

<script>
import { API_BASE_URL } from '../config'

export default {
  data() {
    return {
      username: null,
      messageText: '',
      messages: [],
      ws: null,
    };
  },
  created() {
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/user/me`, {
          method: 'GET',
          credentials: 'include'
        });
        const userInfo = await response.json();
        this.username = userInfo.username;

        if (this.username) {
          this.initWebSocket();
          this.fetchLastMessages();
        }
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    },
    async initWebSocket() {
      this.ws = new WebSocket(`ws://localhost:8000/chat/ws/${this.username}`);
      this.ws.onmessage = this.handleMessage;
    },
    async fetchLastMessages() {
      try {
        const response = await fetch(`${API_BASE_URL}/chat/last_messages`, {
          method: 'GET'
        });
        this.messages = await response.json();
      } catch (error) {
        console.error('Error fetching last messages:', error);
      }
    },
    appendMessage(msg) {
      this.messages.push({ content: msg });
    },
    sendMessage() {
      const messageData = {
        username: this.username,
        message: this.messageText,
      };
      this.ws.send(JSON.stringify(messageData));
    
      // Update messages directly instead of reloading the page
      this.appendMessage(this.messageText);
      this.messageText = '';
    },
  }
};
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1, h2 {
  text-align: center;
}

h2 span {
  font-weight: bold;
  color: #007BFF; /* Blue color for the client ID */
}

.message-form {
  display: flex;
  margin-top: 15px;
}

.message-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 8px;
}

.send-button {
  background-color: #28A745; /* Green color for the send button */
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.send-button:hover {
  background-color: #218838; /* Darker green on hover */
}

.message-list {
  list-style: none;
  padding: 0;
  margin: 15px 0 0;
}

.message {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px;
  margin-bottom: 8px;
}

/* Add additional styles as needed */
</style>