<template>
  <div>
    <div>
      <label for="start-date">Start Date:</label>
      <input type="date" id="start-date" v-model="startDate" @change="filterTransactions" />
      <label for="end-date">End Date:</label>
      <input type="date" id="end-date" v-model="endDate" @change="filterTransactions" />
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>From</th>
            <th>To</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in filteredTransactions" :key="transaction.id">
            <td>{{ transaction.date }}</td>
            <td>{{ transaction.sender }}</td>
            <td>{{ transaction.receiver }}</td>
            <td>{{ transaction.amount }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      <button @click="fetchTransactions" class="refresh-button">Refresh</button>
    </div>
  </div>
</template>

<!-- TransactionsTable.vue -->
<script setup>
import { ref, onMounted, onUnmounted, watchEffect } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const transactions = ref([])
const filteredTransactions = ref([])
// const userType = store.userType;
const currentPage = ref(1)
const totalPages = ref(1)
const startDate = ref('')
const endDate = ref('')
// const perPage = ref(10);
const timerId = ref(null)

const fetchTransactions = async () => {
  try {
    const response = await fetch('/api/accounts/transactions', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${store.state.sessionId}`,
        'Content-Type': 'application/json'
      }
      // params: { page: this.currentPage, userType: this.userType }
    })
    console.log('Hello, fetch transactions')
    const data = await response.json()
    console.log(data.message)
    if (data.status === 'success') {
      console.log(data)
      transactions.value = data.transactions
      filteredTransactions.value = data.transactions
      totalPages.value = data.totalPages
    }
  } catch (error) {
    console.log(error)
  }
}

const filterTransactions = () => {
  if (!startDate.value && !endDate.value) {
    filteredTransactions.value = transactions.value
  } else {
    const start = new Date(startDate.value)
    const end = new Date(endDate.value)
    filteredTransactions.value = transactions.value.filter(
      (transaction) =>
        (!startDate.value || new Date(transaction.date) >= start) &&
        (!endDate.value || new Date(transaction.date) <= end)
    )
  }
}

const prevPage = async () => {
  if (currentPage.value > 1) {
    currentPage.value--
    await fetchTransactions()
  }
}

const nextPage = async () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    await fetchTransactions()
  }
}

onMounted(async () => {
  await fetchTransactions()

  timerId.value = setInterval(async () => {
    await fetchTransactions()
  }, 10000)

  watchEffect(async () => {
    if (store.state.refreshTransactions) {
      await fetchTransactions()
      store.commit('setRefreshTransactions', false)
    }
  })
})

onUnmounted(() => {
  clearInterval(timerId.value)
})
</script>

<style scoped>
.table-container {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}

.pagination button {
  background-color: #4caf50;
  border: none;
  color: white;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin: 0 4px;
  cursor: pointer;
  border-radius: 4px;
}

.pagination button:hover {
  background-color: #45a049;
}

.pagination button[disabled] {
  background-color: #999999;
  cursor: not-allowed;
}

.refresh-button {
  background-color: #4caf50;
  border: none;
  color: white;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin: 10px 2px;
  cursor: pointer;
  border-radius: 4px;
}

.refresh-button:hover {
  background-color: #45a049;
}
</style>
