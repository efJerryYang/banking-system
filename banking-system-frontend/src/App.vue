<script setup>
// import { RouterView } from 'vue-router'
import LoginPage from './components/LoginPage.vue'
</script>

<template>
  <div class="welcome-page">
    <header>
      <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
    </header>
    <div class="login-container">
      <LoginPage/>
    </div>
  </div>
</template>

<style scoped>
.welcome-page {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-image: url("@/assets/bank-full-length.png");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  filter: brightness(1.2);
}

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
