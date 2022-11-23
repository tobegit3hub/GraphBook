import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from "vue-router";
import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'
import axios from 'axios'
import "echarts"

import App from './App.vue'
import TopicList from './components/TopicList.vue';
import GraphDetail from './components/GraphDetail.vue';
import ComputePaths from './components/ComputePaths.vue'
import CharactersCards from './components/CharactersCards.vue'
import SelectCharacters from './components/SelectCharacters.vue';
import CharacterDetail from './components/CharacterDetail.vue'
import EditTopics from './components/EditTopics.vue';
import EditGraph from './components/EditGraph.vue';
import AddCharacterWizard from './components/AddCharacterWizard.vue';
import EditCharacters from './components/EditCharacters.vue';
import EditRelations from './components/EditRelations.vue';
import EditGroups from './components/EditGroups.vue';

// Read config from .env.development and .env.production to set global server endpoint
axios.defaults.baseURL = import.meta.env.VITE_API_ENDPOINT;

function useTable (app) {
  app.use(VXETable)
}

const routes = [
  { path: '/', component: TopicList },
  { path: '/topics/:topic/graph', component: GraphDetail, props: true },
  { path: '/topics/:topic/characters', component: SelectCharacters, props: true,
    children: [
      { path: ':character_name', component: CharacterDetail, props: true}
    ]
  },
  { path: '/topics/:topic/edit', component: EditGraph, props: true,
    children: [
      { path: 'addcharacter', component: AddCharacterWizard, props: true },
      { path: 'characters', component: EditCharacters, props: true },
      { path: 'relations', component: EditRelations, props: true },
      { path: 'groups', component: EditGroups, props: true }
    ]
  },
  { path: '/topics/:topic/cards', component: CharactersCards, props: true },
  { path: '/topics/:topic/paths', component: ComputePaths, props: true },
  { path: '/topics/edit', component: EditTopics, props: true }
]
 
 const router = createRouter({
  history:createWebHashHistory('/'),
  routes
 })

const app = createApp(App)
app.use(useTable)
app.use(router)
app.mount('#app')
