import './assets/main.css'
import './assets/global.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'

import VueToastify from 'vue-toastify'
import 'vue-toastify/index.css'
axios.defaults.baseURL = '/'

const app = createApp(App)

app.use(router)
app.use(store)
app.use(VueToastify)

app.mount('#app')
