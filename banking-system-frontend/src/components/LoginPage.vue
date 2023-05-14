<template>
  <div class="container">
    <h1>Login Page</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" class="form-control" id="username" v-model="username" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" />
      </div>
      <div>
        <div v-if="showMessage" :class="['message', messageType]">{{ message }}</div>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { loadClientId } from '../utils/utils'
import { useRouter } from 'vue-router'
import useMessageHandler from '../composables/useMessageHandler'

import {toast} from 'vue3-toastify'

const store = useStore()
const router = useRouter()
const username = ref('')
const password = ref('')

const { message, messageType, showMessage, displayMessage, clearMessage } = useMessageHandler()

const submitForm = async () => {
  clearMessage()
  const clientId = loadClientId()
  console.log('Client ID:', clientId)
  if (store.state.sessionId) {
    console.log('Already logged in')
    displayMessage('Already logged in', 'error')
    router.push('/dashboard')
    return
  }
  await store.dispatch('login', {
    username: username.value,
    password: password.value,
    clientId: clientId
  })
  console.log('Username:', username.value)
  console.log('Password:', password.value)
  if (store.state.sessionId) {
    console.log('Logged in')
    displayMessage('Logged in', 'success')
    store.state.showLoginNotification = true
    router.push('/dashboard')
  } else {
    console.log('Not logged in')
    displayMessage('Invalid username or password', 'error')
  }
}

onMounted(() => {
  if (store.state.showLogoutNotification) {
    toast.info('You have been logged out', {position:'top-center'})
    store.state.showLogoutNotification = false
  }
})
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
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
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

.form-control {
  display: block;
  width: 100%;
  padding: 6px 12px;
  font-size: 14px;
  line-height: 1.42857143;
  color: #020202;
  background-color: #fff;
  background-image: none;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  display: inline-block;
  margin-bottom: 0;
  font-weight: normal;
  text-align: center;
  vertical-align: middle;
  touch-action: manipulation;
  cursor: pointer;
  background-image: none;
  border: 1px solid transparent;
  white-space: nowrap;
  padding: 6px 12px;
  font-size: 14px;
  line-height: 1.42857143;
  border-radius: 4px;
}

.btn-primary {
  color: #fff;
  background-color: #337ab7;
  border-color: #2e6da4;
}

.btn-primary:hover {
  background-color: #286090;
  border-color: #204d74;
}
</style>
