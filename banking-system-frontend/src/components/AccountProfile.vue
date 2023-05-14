<!-- AccountProfile.vue -->
<template>
  <div>
    <ul class="nav">
      <li class="nav-item">
        <router-link to="/account/balance" v-slot="{ isActive }">
          <a :class="{ 'router-link-active': isActive }">Account Balance</a>
        </router-link>
      </li>
      <li class="nav-item">
        <router-link to="/account/transfer" v-slot="{ isActive }">
          <a :class="{ 'router-link-active': isActive }">Transfer Funds</a>
        </router-link>
      </li>
    </ul>
    <router-view></router-view>
  </div>
</template>

<script setup></script>

<style scoped>
.nav {
  display: flex;
  justify-content: space-around;
  list-style-type: none;
  padding: 0;
  margin-bottom: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.nav-item {
  padding: 1rem;
}

.nav-item a {
  text-decoration: none;
  color: #495057;
  font-weight: bold;
}

.nav-item a:hover {
  color: #007bff;
}

.nav-item a.router-link-active {
  font-weight: 900;
  background-color: #e9ecef;
  border-radius: 5px;
  padding: 0.5rem 1rem;
}
</style>
