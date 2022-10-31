import { createApp } from 'vue'
import App from './App.vue'

import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'

function useTable (app) {
    app.use(VXETable)
  }

//import './assets/main.css'

import "echarts"

//createApp(App).mount('#app')
createApp(App).use(useTable).mount('#app')

