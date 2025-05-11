// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import i18n from './i18n'

// 设置 axios
axios.defaults.baseURL = ''

const app = createApp(App)
app.config.globalProperties.$axios = axios

app.use(router).use(ElementPlus).use(i18n).mount('#app')