import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/components/LoginPage.vue'
import TheDashboard from '@/components/TheDashboard.vue'
import CreateAccount from '@/components/CreateAccount.vue'
import DeleteAccount from '@/components/DeleteAccount.vue'
import AccountBalance from '@/components/AccountBalance.vue'
import TransferFunds from '@/components/TransferFunds.vue'

import store from '@/store'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: TheDashboard
  },
  {
    path: '/create-account',
    name: 'create-account',
    component: CreateAccount
  },
  {
    path: '/delete-account',
    name: 'delete-account',
    component: DeleteAccount
  },
  {
    path: '/account-balance',
    name: 'account-balance',
    component: AccountBalance
  },
  {
    path: '/transfer-funds',
    name: 'transfer-funds',
    component: TransferFunds
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  if (to.path === '/logout') {
    await store.dispatch('logout')
    next('/login')
  } else {
    next()
  }
})

export default router
