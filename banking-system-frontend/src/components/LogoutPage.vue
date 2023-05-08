<template>
  <div class="container">
    <h1>Logout Page</h1>
    <button class="btn btn-primary" @click="logout">Logout</button>
  </div>
</template>

<script setup>
const logout = () => {
  // TODO
  // Clear session and notify server
  console.log('User logged out');
};
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
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
