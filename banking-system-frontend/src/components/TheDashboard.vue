<template>
  <div class="dashboard">
    <h1>The Dashboard</h1>
    <div class="actions">
      <router-link to="/create-account" class="action">Create Account</router-link>
      <router-link :to="userType === 'customer' ? `/delete-account/${username}` : '/delete-account'" class="action">Delete
        Account</router-link>
      <router-link to="/account-balance" class="action">Account Balance</router-link>
      <router-link to="/transfer-funds" class="action">Transfer Funds</router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const userType = store.state.userType;
const username = store.state.username;

onMounted(() => {
  store.dispatch('getUserType');
});
</script>

<style scoped>
.dashboard {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}


.actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.action {
  background-color: #337ab7;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  text-decoration: none;
  margin: 10px;
}

.action:hover {
  background-color: #286090;
}
</style>
