<template>
  <main class="chat-page">
    <h1>Chat</h1>
    <h2>Your ID: <span id="ws-id">{{ clientId }}</span></h2>
    <form @submit.prevent="sendMessage">
      <input v-model="messageText" type="text" autocomplete="off" />
      <button>Send</button>
    </form>
    <ul id="messages">
      <li v-for="message in messages" :key="message.id">{{ message.content }}</li>
    </ul>
  </main>
</template>

<script>
export default {
  data() {
    return {
      clientId: Date.now(),
      messageText: '',
      messages: [],
      ws: null,
    };
  },
  mounted() {
    this.fetchLastMessages().then((messages) => {
      this.messages = messages;
    });

    this.connectWebSocket();
  },
  methods: {
    async fetchLastMessages() {
      const response = await fetch('http://localhost:8000/chat/last_messages', {
        method: 'GET',
      });
      return response.json();
    },
    appendMessage(msg) {
      this.messages.push({ id: Date.now(), content: msg });
    },
    connectWebSocket() {
      this.ws = new WebSocket(`ws://localhost:8000/chat/ws/${this.clientId}`);
      this.ws.onmessage = (event) => {
        this.appendMessage(event.data);
      };
    },
    sendMessage() {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(this.messageText);
        this.messageText = '';
      }
    },
  },
};
</script>
