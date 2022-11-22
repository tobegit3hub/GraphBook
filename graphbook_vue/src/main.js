import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from "vue-router";
import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'
//import './assets/main.css'
import "echarts"

import App from './App.vue'
import GraphDetail from './components/GraphDetail.vue';
import EditGraph from './components/EditGraph.vue';
import ComputeNodesPath from './components/ComputeNodesPath.vue'
import CharactersCards from './components/CharactersCards.vue';
import CharacterDetail from './components/CharacterDetail.vue';
import TopicList from './components/TopicList.vue';

function useTable (app) {
  app.use(VXETable)
}

const routes = [
  { path: '/', component: TopicList },
  { path: '/topics/:topic', component: GraphDetail },
]
 
 const router = createRouter({
  history:createWebHashHistory('/'),
  routes
 })

const app = createApp(App)
app.use(useTable)
app.use(router)
app.mount('#app')
