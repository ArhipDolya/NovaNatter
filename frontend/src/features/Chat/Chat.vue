<template>
  <div class="chat-container">
    <h1>NovaNatter Chat</h1>
    <h2>Your username: <span>{{ username }}</span></h2>
    <form @submit.prevent="sendMessage" class="message-form">
      <input v-model="messageText" type="text" autocomplete="off" class="message-input" />
      <button type="submit" class="send-button">Send</button>
    </form>
    <ul class="message-list">
      <li v-for="(message, index) in messages" :key="index" class="message">
        <div class="user-info">
          <UserAvatar />
          <MessageContent :message="message.message" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import UserAvatar from './UserAvatar.vue';
import MessageContent from './MessageContent.vue';
import { API_BASE_URL } from '../config';
import axios from 'axios'

interface Message {
  message: string;
}

export default defineComponent({
  components: {
    UserAvatar,
    MessageContent,
  },
  data() {
    return {
      username: null as string | null,
      messageText: '',
      messages: [] as Message[],
      ws: null as WebSocket | null,
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

        if (!response.ok) {
          document.location.href = '/login';
          return;
        }

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
    initWebSocket() {
      this.ws = new WebSocket(`ws://localhost:8000/chat/ws/${this.username}`);
      this.ws.onmessage = this.handleMessage;
    },
    async fetchLastMessages() {
      const response = await fetch('http://localhost:8000/chat/last_messages');
      const messages = await response.json();
      this.messages = messages;
    },
    appendMessage(msg: string) {
      this.messages.push({ message: msg });
    },
    sendMessage() {
      if (this.ws) {
        const messageData = {
          username: this.username,
          message: this.messageText,
        };
        this.ws.send(JSON.stringify(messageData));
      }

      this.appendMessage(this.messageText);
      this.messageText = '';

      setTimeout(() => {
        location.reload();
      }, 500);
    },
    handleMessage(event: MessageEvent) {
      const message = JSON.parse(event.data);
      this.appendMessage(message.message);
    },
  },
});
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: auto;
  padding: 50px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1, h2 {
  text-align: center;
}

h2 span {
  font-weight: bold;
  color: #007BFF;
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
  background-color: #28A745;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.send-button:hover {
  background-color: #218838;
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

.user-info {
  display: flex;
  align-items: center;
}
</style>