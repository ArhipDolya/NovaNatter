<template>
  <div class="chat-container">
    <h1>WebSocket Chat</h1>
    <h2>Your ID: <span>{{ clientId }}</span></h2>
    <form @submit.prevent="sendMessage" class="message-form">
      <input v-model="messageText" type="text" autocomplete="off" class="message-input" />
      <button type="submit" class="send-button">Send</button>
    </form>
    <ul class="message-list">
      <li v-for="(message, index) in messages" :key="index" class="message">{{ message.message }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      clientId: Date.now(),
      messageText: '',
      messages: [],
      ws: new WebSocket(`ws://localhost:8000/chat/ws/${Date.now()}`),
      refreshFlag: false // Add a flag to trigger refresh
    };
  },
  created() {
    this.fetchLastMessages();
    this.ws.onmessage = this.handleMessage;
  },
  watch: {
    refreshFlag() {
      // Watch for changes in refreshFlag and fetch messages
      this.fetchLastMessages();
    }
  },
  methods: {
    async fetchLastMessages() {
      const response = await fetch('http://localhost:8000/chat/last_messages', {
        method: 'GET'
      });
      const messages = await response.json();
      this.messages = messages;
    },
    appendMessage(msg) {
      this.messages.push({ content: msg });
    },
    sendMessage() {
      this.ws.send(this.messageText);
      this.messageText = '';

      // Toggle the refreshFlag to trigger a refresh
      this.refreshFlag = !this.refreshFlag;
    },
    handleMessage(event) {
      console.log("Received message:", event.data);
      this.appendMessage(event.data);
    }
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