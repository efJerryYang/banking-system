<template>
  <div class="transfer-funds-container">
    <h1>Transfer Funds</h1>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const destAccountId = ref('')
const amount = ref('')

async function transferFunds() {
  if (!destAccountId.value || !amount.value) {
    alert('Please enter a destination account ID and transfer amount')
    return
  }

  const sessionId = store.state.sessionId
  const sourceAccountId = store.state.accountId

  try {
    const response = await fetch(`/api/accounts/${sourceAccountId}/transfer`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${sessionId}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sessionId,
        sourceAccountId,
        destAccountId: destAccountId.value,
        amount: parseFloat(amount.value)
      })
    })

    const data = await response.json()

    if (data.status === 'success') {
      alert('Funds transferred successfully')
      destAccountId.value = ''
      amount.value = ''
    } else {
      alert('Error transferring funds: ' + data.message)
    }
  } catch (error) {
    alert('Error transferring funds: ' + error.message)
  }
}
</script>

<style scoped>
.transfer-funds-container {
  max-width: 500px;
  margin: 0 auto;
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
