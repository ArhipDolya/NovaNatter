<template>
  <div class="profile-container">
    <h1>Profile</h1>
    <div v-if="username && userImage" class="username-info">
      <img :src="userImage" alt="User Avatar" class="user-avatar" />
      <span class="username-text">Username: {{ username }}</span>
    </div>

    <form @submit.prevent="uploadImage" class="upload-form">

      <label for="fileInput" class="custom-file-label">
        <input id="fileInput" type="file" accept="image/*" @change="handleFileChange" class="hidden-input" />
        Choose File
      </label>

      <button type="submit" :disabled="!selectedFile" class="upload-button">Upload Image</button>
    </form>

  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../config';

export default {
  setup() {
    const username = ref<string | null>('');
    const userImage = ref<string | null>('');
    const selectedFile = ref<string | null>(null)

    // Function to fetch user information on component mount
    const getUserInfo = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/user/me`, {
          credentials: 'include',
        });

        if (response.ok) {
          const userInfo = await response.json();
          username.value = userInfo.username;
          userImage.value = `${API_BASE_URL}/images/${userInfo.profile_image}`;
        } else {
          console.error('Failed to fetch user info');
        }
      } catch (error) {
        console.error('Error during fetch:', error.message);
      }
    };

    // Function to handle file change event
    const handleFileChange = (event: Event) => {
      const inputElement = event.target as HTMLInputElement;
      const files = inputElement.files

      if (files && files.length > 0) {
        selectedFile.value = files[0];
      }
    } 

    // Function to upload the selected image file
    const uploadImage = async () => {
      if (selectedFile.value) {
        const formData = new FormData();
        formData.append('file', selectedFile.value)

        try {
          const response = await fetch(`${API_BASE_URL}/auth/user/uploadfile`, {
            method: 'POST',
            body: formData,
            credentials: 'include',
          });

          if (response.ok) {
            // Refresh user info after successful upload
            await getUserInfo();
          } else {
            console.error('Failed to upload image');
          }
        } catch(error) {
          console.error('Error during image upload:', error.message);
        }
      }
    }

    onMounted(getUserInfo);

    return {
      username,
      userImage,
      selectedFile,
      handleFileChange,
      uploadImage,
    };
  },
};
</script>
  
<style scoped>
.profile-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  font-size: 1.5rem;
  margin-bottom: 20px;
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

.upload-form {
  margin-top: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-file-label {
  cursor: pointer;
  display: inline-block;
  padding: 10px 20px;
  background-color: #3498db;
  color: #fff;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.custom-file-label:hover {
  background-color: #2980b9;
}

.hidden-input {
  display: none;
}

.upload-button {
  margin-left: 20px;
  background-color: #2ecc71;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.upload-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.upload-button:hover:enabled {
  background-color: #27ae60;
}
</style>