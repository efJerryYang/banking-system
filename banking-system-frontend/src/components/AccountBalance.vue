<template>
  <div class="account-balance-container">
    <h1>Account Balance</h1>
    <router-link to="/dashboard" class="back-to-dashboard">Back to Dashboard</router-link>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <p>Your current account balance is: {{ balance }}</p>
      <button @click="refreshBalance">Refresh Balance</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
const balance = ref(0)
const loading = ref(true)
// if the user is not logged in, redirect to the login page
if (!store.state.sessionId) {
  router.push('/login')
}

async function fetchAccountBalance() {
  const sessionId = store.state.sessionId

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
      balance.value = data.balance
    } else {
      alert('Error fetching account balance: ' + data.message)
    }
  } catch (error) {
    alert('Error fetching account balance: ' + error.message)
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
