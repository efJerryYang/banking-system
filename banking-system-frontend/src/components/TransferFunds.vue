<template>
  <div class="transfer-funds-container">
    <h1>Transfer Funds</h1>
    <router-link to="/dashboard" class="back-to-dashboard">Back to Dashboard</router-link>
    <form @submit.prevent="transferFunds">
      <div class="form-group">
        <label for="destAccountId">Destination Account ID:</label>
        <input
          type="text"
          id="destAccountId"
          v-model="destAccountId"
          placeholder="Enter destination account ID"
          required
        />
      </div>
      <div class="form-group">
        <label for="amount">Transfer Amount:</label>
        <input
          type="number"
          id="amount"
          v-model="amount"
          step="0.01"
          placeholder="Enter transfer amount"
          required
        />
      </div>
      <button type="submit">Transfer Funds</button>
    </form>
    <div v-if="showMessage" :class="['message', messageType]">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import useMessageHandler from '../composables/useMessageHandler'

const store = useStore()
const router = useRouter()
const destAccountId = ref('')
const amount = ref('')

const { message, messageType, showMessage, displayMessage, clearMessage } = useMessageHandler()

// if the user is not logged in, redirect to the login page
if (!store.state.sessionId) {
  router.push('/login')
}

async function transferFunds() {
  clearMessage()
  if (!destAccountId.value || !amount.value) {
    // alert('Please enter a destination account ID and transfer amount')
    displayMessage('Please enter a destination account ID and transfer amount')
    return
  }

  const sessionId = store.state.sessionId

  try {
    const response = await fetch(`/api/accounts/transfer`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${sessionId}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        destAccountId: destAccountId.value,
        amount: parseFloat(amount.value)
      })
    })

    const data = await response.json()

    if (data.status === 'success') {
      // alert('Funds transferred successfully')
      displayMessage('Funds transferred successfully', 'success')
      destAccountId.value = ''
      amount.value = ''
    } else {
      // alert('Error transferring funds: ' + data.message)
      displayMessage('Error transferring funds: ' + data.message)
    }
  } catch (error) {
    // alert('Error transferring funds: ' + error.message)
    displayMessage('Error transferring funds: ' + error.message)
  }
}
</script>

<style scoped>
.transfer-funds-container {
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
