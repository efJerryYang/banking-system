<template>
  <div class="delete-account-container">
    <h1>Delete Account</h1>
    <router-link to="/dashboard" class="back-to-dashboard">Back to Dashboard</router-link>
    <div class="message" v-if="showMessage" :class="messageType">{{ message }}</div>
    <form @submit.prevent="deleteAccount">
      <div class="form-group">
        <label for="accountId">Account ID:</label>
        <input
          type="text"
          id="accountId"
          v-model="accountId"
          placeholder="Enter account ID to delete"
          required
        />
      </div>
      <button type="submit">Delete Account</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import useMessageHandler from '../composables/useMessageHandler'

const store = useStore()
const router = useRouter()
const accountId = ref('')

const { message, messageType, showMessage, displayMessage, clearMessage } = useMessageHandler()

// if the user is not logged in, redirect to the login page
if (!store.state.sessionId) {
  router.push('/login')
}

async function deleteAccount() {
  clearMessage()
  if (!accountId.value) {
    displayMessage('Please enter the account ID to delete')
    return
  }

  const sessionId = store.state.sessionId

  try {
    const response = await fetch(`/api/accounts/${accountId.value}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${sessionId}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()

    if (data.status === 'success') {
      displayMessage('Account deleted successfully', 'success')
      accountId.value = ''
    } else {
      displayMessage('Error deleting account: ' + data.message)
    }
  } catch (error) {
    displayMessage('Error deleting account: ' + error.message)
  }
}
</script>

<style scoped>
.delete-account-container {
  max-width: 500px;
  margin: 0 auto;
}

.message {
  padding: 0.5rem 1rem;
  margin-bottom: 1rem;
  border-radius: 5px;
}

.success {
  background-color: #d4edda;
  color: #155724;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background-color: #45a049;
}
</style>
