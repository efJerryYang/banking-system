import './assets/main.css'
import './assets/global.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'
import Vue3Toasity, { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

axios.defaults.baseURL = '/'

const app = createApp(App)

app.use(router)
app.use(store)
app.use(Vue3Toasity, {
    delay: 0,
    autoClose: 1000,
    hideProgressBar: true,
    transition: toast.TRANSITIONS.BOUNCE,
    multiple: false,
})

app.mount('#app')
