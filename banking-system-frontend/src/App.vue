<script setup></script>

<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

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
