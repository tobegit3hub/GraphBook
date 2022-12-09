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
  English: {
    message: {
      // Home
      Home: 'Home',
      Graph: 'Graph',
      Characters: "Characters",
      Edit: "Edit",
      Cards: "Cards",
      Paths: "Paths",
      Topics: "Topics",
      Languages: "Language",
      PleaseChooseTopic: "Please choose topic",
      TopicsList: "Topics List",
      Reset: "Reset",
      SearchFromTopics: "Search from {topic_count} topics",
      // Graph
      Groups: "Groups",
      GraphAnimation: "Graph Animation",
      Play: "Play",
      Stop: "Stop",
      GraphParameters: "Graph Parameters",
      ChooseAll: "Choose All",
      Name: "Name",
      Weight: "Weight",
      Note: "Note",
      ImageMode: "Image Mode",
      RoamScaleMode: "ROAM Scale Mode",
      CharactrWeightMode: "Character Weight Mode",
      CharactrSize: "Character Size",
      CharacterFontSize: "Character Font Size",
      RelationFontSize: "Relation Font Size",
      ShadowSize: "Shadow Size",
      LineWidth: "Line Width",
      LineCurveness: "Line Curveness",
      // Characters
      Choose: "Choose",
      CharacterAssociation: "Character Association",
      Upstream: "Upstream",
      Downstream: "Downstream",
      // Edit
      // Paths
      Compute: "Compute",
      // Topics
      Manage: "Manage",
      Export: "Export",
      Import: "Import",
      All: "All",
      Official: "Official",
      NotOfficial: "Not official",
    }
  },
  简体中文: {
    message: {
      // Home
      Home: '首页',
      Graph: '关系图',
      Characters: "角色",
      Edit: "编辑",
      Cards: "卡片",
      Paths: "路径",
      Topics: "主题",
      Languages: "语言",
      PleaseChooseTopic: "请选择主题",
      TopicsList: "主题列表",
      Reset: "重置",
      SearchFromTopics: "从 {topic_count} 个主题中搜索",
      // Graph
      Groups: "分组",
      GraphAnimation: "关系图动画",
      Play: "播放",
      Stop: "暂停",
      GraphParameters: "关系图参数",
      ChooseAll: "选择全部",
      Name: "名字",
      Weight: "权重",
      Note: "备注",
      ImageMode: "图片模式",
      RoamScaleMode: "ROAM缩放模式",
      CharactrWeightMode: "角色权重模式",
      CharactrSize: "角色大小",
      CharacterFontSize: "角色字体大小",
      RelationFontSize: "关系字体大小",
      ShadowSize: "阴影大小",
      LineWidth: "线宽",
      LineCurveness: "线曲度",
      // Characters
      Choose: "选择",
      CharacterAssociation: "关联角色",
      Upstream: "上游",
      Downstream: "下游",
      // Edit
      // Paths
      Compute: "计算",
      // Topics
      Manage: "管理",
      Export: "导出",
      Import: "导入",
      All: "所有",
      Official: "官方",
      NotOfficial: "非官方",
    }
  }
}

const i18n = createI18n({
  locale: '简体中文',
  fallbackLocale: 'en',
  messages
})

const app = createApp(App)
app.use(router)
app.use(useTable)
app.use(i18n)
app.mount('#app')
