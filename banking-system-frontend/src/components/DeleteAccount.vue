<template>
  <div class="delete-account-container">
    <h1>Delete Account</h1>
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

const store = useStore()
const accountId = ref('')

async function deleteAccount() {
  if (!accountId.value) {
    alert('Please enter the account ID to delete')
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
      alert('Account deleted successfully')
      accountId.value = ''
    } else {
      alert('Error deleting account: ' + data.message)
    }
  } catch (error) {
    alert('Error deleting account: ' + error.message)
  }
}
</script>

<style scoped>
.delete-account-container {
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
