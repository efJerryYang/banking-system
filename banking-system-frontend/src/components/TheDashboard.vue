<template>
  <div class="dashboard">
    <h1>The Dashboard</h1>
    <div class="grid-container">
      <div v-for="(link, index) in actionLinks" :key="index" class="grid-item">
        <router-link :to="link.to" class="action">
          <span>{{ link.text }}</span>
        </router-link>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import {toast} from 'vue3-toastify'

const store = useStore()
const router = useRouter()
const userType = store.state.userType
const username = store.state.username

// if the user is not logged in, redirect to the login page
if (!store.state.sessionId) {
  router.push('/login')
}

const actionLinks = [
  userType === 'clerk' ? { text: 'Create Account', to: '/create-account' } : null,
  userType === 'clerk'
    ? {
        text: 'Delete Account',
        to: userType === 'customer' ? `/delete-account/${username}` : '/delete-account'
      }
    : null,
  { text: 'Account Balance', to: '/account-balance' },
  { text: 'Transfer Funds', to: '/transfer-funds' }
].filter((link) => link !== null)

onMounted(() => {
  // store.dispatch('getUserType')
  if (store.state.showLoginNotification) {
    toast.info('Login successful!',{position: 'top-center'})
    store.state.showLoginNotification = false
  }
})
</script>

<style scoped>
.dashboard {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 10px;
}

.grid-item {
  padding: 0.5rem 1rem;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  text-decoration: none;
  margin: 10px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.grid-item:hover {
  background-color: #45a049;
}

.action {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  text-decoration: none;
}
</style>
