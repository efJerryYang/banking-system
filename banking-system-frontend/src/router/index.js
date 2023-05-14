import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/components/LoginPage.vue'
import TheDashboard from '@/components/TheDashboard.vue'
import CreateAccount from '@/components/CreateAccount.vue'
import DeleteAccount from '@/components/DeleteAccount.vue'
import AccountBalance from '@/components/AccountBalance.vue'
import TransferFunds from '@/components/TransferFunds.vue'

import LogoutHandler from '@/components/LogoutHandler.vue'

import AccountProfile from '@/components/AccountProfile.vue'

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
    path: '/logout',
    name: 'logout',
    component: LogoutHandler
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
    path: '/account',
    name: 'account-profile',
    component: AccountProfile,
    children: [
      {
        path: '/account/balance',
        name: 'account-balance',
        component: AccountBalance
      },
      {
        path: '/account/transfer',
        name: 'transfer-funds',
        component: TransferFunds
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
