import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import { createRouter, createWebHashHistory } from "vue-router";
import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'
import axios from 'axios'
import "echarts"

import App from './App.vue'
import HomeTopicList from './components/HomeTopicList.vue';
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
import ChooseTopic from './components/ChooseTopic.vue';

// Read config from .env.development and .env.production to set global server endpoint
axios.defaults.baseURL = import.meta.env.VITE_API_ENDPOINT;

function useTable(app) {
  app.use(VXETable)
}

const routes = [
  { path: '/', component: HomeTopicList },
  { path: '/topics/:topic/graph', component: GraphDetail, props: true },
  // TODO: Use redirect if possible
  { path: '/topics/:topic', component: GraphDetail, props: true },
  {
    path: '/topics/:topic/characters', component: SelectCharacters, props: true,
    children: [
      { path: ':character_name', component: CharacterDetail, props: true }
    ]
  },
  {
    path: '/topics/:topic/edit', component: EditGraph, props: true,
    children: [
      { path: 'addcharacter', component: AddCharacterWizard, props: true },
      { path: 'characters', component: EditCharacters, props: true },
      { path: 'relations', component: EditRelations, props: true },
      { path: 'groups', component: EditGroups, props: true }
    ]
  },
  { path: '/topics/:topic/cards', component: CharactersCards, props: true },
  { path: '/topics/:topic/paths', component: ComputePaths, props: true },
  { path: '/topics/edit', component: EditTopics, props: true },
  { path: '/topics/choose', component: ChooseTopic },
  { path: '/404', redirect: "/topics/choose" },
  { path: '/:pathMatch(.*)*', redirect: "/404" }
]

const router = createRouter({
  history: createWebHashHistory('/'),
  routes
})


const messages = {
  en: {
    message: {
      Home: 'Home',
      Graph: 'Graph',
      Characters: "Characters",
      Edit: "Edit",
      Cards: "Cards",
      Paths: "Paths",
      Topics: "Topics",

      PleaseChooseTopic: "Please choose topic",
      TopicsList: "Topics List",

      Reset: "Reset",
      SearchFrom: "Search from",
      topics: "topics",

      Groups: "Groups",
      PlayGraphAnimation: "Play graph animation",
      Play: "Play",
      Stop: "Stop",

      Choose: "Choose",
      CharacterAssociation: "Character Association",
      Upstream: "Upstream",
      Downstream: "Downstream",

      Compute: "Compute",

      Manage: "Manage",
      Export: "Export",
      Import: "Import",
      All: "All",
      Official: "Official",
      NotOfficial: "Not official",
    }
  },
  zh: {
    message: {
      Home: '首页',
      Graph: '关系图',
      Characters: "角色",
      Edit: "编辑",
      Cards: "卡片",
      Paths: "路径",
      Topics: "主题",

      PleaseChooseTopic: "请选择主题",
      TopicsList: "主题列表",

      Reset: "重制",
      SearchFrom: "搜索自",
      topics: "主题",

      Groups: "分组",
      PlayGraphAnimation: "Play graph animation",
      Play: "Play",
      Stop: "Stop",

      Choose: "Choose",
      CharacterAssociation: "Character Association",
      Upstream: "Upstream",
      Downstream: "Downstream",

      Compute: "Compute",

      Manage: "Manage",
      Export: "Export",
      Import: "Import",
      All: "All",
      Official: "Official",
      NotOfficial: "Not official",
    }
  }
}

const i18n = createI18n({
  locale: 'zh',
  fallbackLocale: 'en',
  messages
})

const app = createApp(App)
app.use(router)
app.use(useTable)
app.use(i18n)
app.mount('#app')
