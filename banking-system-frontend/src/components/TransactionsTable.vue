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
            <td>{{ transaction.from }}</td>
            <td>{{ transaction.to }}</td>
            <td>{{ transaction.amount }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<!-- TransactionsTable.vue -->
<script setup>
import { ref, onMounted } from 'vue'
// import { useStore } from 'vuex';

// const store = useStore();

const transactions = ref([])
const filteredTransactions = ref([])
// const userType = store.userType;
const currentPage = ref(1)
const totalPages = ref(1)
const startDate = ref('')
const endDate = ref('')
// const perPage = ref(10);

const fetchTransactions = async () => {
  const response = await this.$http.get('/api/transactions', {
    params: { page: this.currentPage, userType: this.userType }
  })
  const data = response.data

  transactions.value = data.transactions
  filteredTransactions.value = data.transactions
  totalPages.value = data.totalPages
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
  justify-content: space-between;
  align-items: center;
}
</style>
