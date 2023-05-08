import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/components/LoginPage.vue'
import LogoutPage from '@/components/LogoutPage.vue'
import TheDashboard from '@/components/TheDashboard.vue'
import CreateAccount from '@/components/CreateAccount.vue'
import DeleteAccount from '@/components/DeleteAccount.vue'
import AccountBalance from '@/components/AccountBalance.vue'
import TransferFunds from '@/components/TransferFunds.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/logout',
    name: 'logout',
    component: LogoutPage
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

export default router

// import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     {
//       path: '/',
//       name: 'home',
//       component: HomeView
//     },
//     {
//       path: '/about',
//       name: 'about',
//       // route level code-splitting
//       // this generates a separate chunk (About.[hash].js) for this route
//       // which is lazy-loaded when the route is visited.
//       component: () => import('../views/AboutView.vue')
//     }
//   ]
// })

// export default router
