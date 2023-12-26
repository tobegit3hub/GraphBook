import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import { createRouter, createWebHashHistory } from "vue-router";
import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'
import axios from 'axios'
import "echarts"
import { VueForceGraph3D } from 'vue-force-graph';


import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';

import en from './locales/en.json'
import zh from './locales/zh.json'

axios.defaults.baseURL = import.meta.env.VITE_API_ENDPOINT;

const i18n = createI18n({
  legacy: false,
  locale: 'zh',
  fallbackLocale: 'en',
  messages: {
      en,
      zh
  }
})

function useTable(app) {
  app.use(VXETable)
}

const app = createApp(App)
app.use(router)
app.use(useTable)
app.use(i18n)
app.use(VueForceGraph3D)
app.mount('#app')
