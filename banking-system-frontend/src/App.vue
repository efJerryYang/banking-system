<template>
  <div class="router-view-container">
    <router-view></router-view>
    <div v-if="store.state.loggedIn" class="user-info">
      <p>Welcome, {{ store.state.username }}</p>
      <a href="#" class="logout" @click.prevent="logout">Logout</a>
    </div>
  </div>
</template>

<script setup>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const logout = async () => {
  console.log('Logging out')
  await store.dispatch('logout')
  console.log('User logged out')
  router.push('/login')
}

if (localStorage.getItem('sessionId')) {
  store.dispatch('setStoreFromLocalStorage')
}
</script>

<style scoped>
header {
  line-height: 1.5;
  width: 100%;

  max-height: 100vh;
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  padding: 1rem 0;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.router-view-container {
  display: flex;
  justify-content: center;
  /* align-items: center; */
  min-height: 100vh;
  padding: 1rem;
  box-sizing: border-box;
}

.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  background-color: rgba(22, 21, 21, 0.6);
}
</style>

<style>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  width: 100%;
  box-sizing: border-box;
}

.router-view-container {
  display: flex;
  justify-content: center;
  /* align-items: center; */
  width: 50%;
  box-sizing: border-box;
}
</style>
