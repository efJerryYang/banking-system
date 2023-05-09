<template>
  <div class="create-account-container">
    <h1>Create Account</h1>
    <router-link to="/dashboard" class="back-to-dashboard">Back to Dashboard</router-link>
    <form @submit.prevent="createAccount">
      <div class="form-group">
        <label for="username">Username:</label>
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="Enter new username"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Enter new password"
          required
        />
      </div>
      <div class="form-group">
        <label for="userType">User Type:</label>
        <select id="userType" v-model="userType" required>
          <option value="" disabled selected>Select user type</option>
          <option value="customer">Customer</option>
          <option value="clerk">Clerk</option>
          <!-- <option value="admin">Admin</option> -->
        </select>
      </div>
      <button type="submit">Create Account</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const userType = ref('')
const sessionId = store.state.sessionId

// if the user is not logged in, redirect to the login page
if (!store.state.sessionId) {
  router.push('/login')
}
async function createAccount() {
  if (!username.value || !userType.value) {
    alert('Please enter a username and select a user type')
    return
  }

  try {
    const response = await fetch('/api/accounts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionId}`
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        userType: userType.value
      })
    })

    const data = await response.json()

    if (data.status === 'success') {
      alert('Account created successfully')
      username.value = ''
      password.value = ''
      userType.value = ''
    } else {
      alert('Error creating account: ' + data.message)
    }
  } catch (error) {
    alert('Error creating account: ' + error.message)
  }
}
</script>

<style scoped>
.create-account-container {
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

input,
select {
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
