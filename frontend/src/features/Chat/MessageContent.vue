<template>
    <div class="message-content">{{ message }}</div>
</template>


<script>
export default {
    props: {
        message: String,
    }
}
</script>

<style scoped>
.message-content {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 8px;
  flex: 1;
}
</style>