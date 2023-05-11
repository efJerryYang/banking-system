<template>
  <div class="account-balance-container">
    <h1>Account Balance</h1>
    <router-link to="/dashboard" class="back-to-dashboard">Back to Dashboard</router-link>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <p>Your current account balance is: {{ balance }}</p>
      <div v-if="showMessage" :class="['message', messageType]">
        {{ message }}
      </div>
      <button @click="refreshBalance">Refresh Balance</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import useMessageHandler from '../composables/useMessageHandler'

const store = useStore()
const router = useRouter()
const balance = ref(0)
const loading = ref(true)

const { message, messageType, showMessage, displayMessage, clearMessage } = useMessageHandler()

// if the user is not logged in, redirect to the login page
if (!store.state.sessionId) {
  router.push('/login')
}

async function fetchAccountBalance() {
  const sessionId = store.state.sessionId
  clearMessage()
  try {
    const response = await fetch(`/api/accounts/balance`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${sessionId}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()

    if (data.status === 'success') {
      displayMessage('Account balance fetched successfully', 'success')
      balance.value = data.balance
    } else {
      displayMessage('Error fetching account balance: ' + data.message, 'error')
    }
  } catch (error) {
    displayMessage('Error fetching account balance: ' + error.message, 'error')
  }

  loading.value = false
}

onMounted(() => {
  fetchAccountBalance()
})
</script>

<style scoped>
.account-balance-container {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
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
