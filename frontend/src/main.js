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
import GroupsList from './components/GroupsList.vue'
import GroupDetail from './components/GroupDetail.vue'
import ChooseCharacters from './components/ChooseCharacters.vue';
import CharacterDetail from './components/CharacterDetail.vue';
import EditTopics from './components/EditTopics.vue';
import EditGraph from './components/EditGraph.vue';
import AddCharacterWizard from './components/AddCharacterWizard.vue';
import EditCharacters from './components/EditCharacters.vue';
import EditRelations from './components/EditRelations.vue';
import EditGroups from './components/EditGroups.vue';
import EditMainlines from './components/EditMainlines.vue';
import ChooseTopic from './components/ChooseTopic.vue';
import MainlineDetail from './components/MainlineDetail.vue';

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
    path: '/topics/:topic/characters', component: ChooseCharacters, props: true,
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
      { path: 'groups', component: EditGroups, props: true },
      { path: 'mainlines', component: EditMainlines, props: true }
    ]
  },
  { path: '/topics/:topic/groups', component: GroupsList, props: true },
  { path: '/topics/:topic/groups/:group', component: GroupDetail, props: true },
  { path: '/topics/:topic/paths', component: ComputePaths, props: true },
  { path: '/topics/edit', component: EditTopics, props: true },
  { path: '/topics/choose', component: ChooseTopic },
  { path: '/topics/:topic/mainlines', component: MainlineDetail, props: true },
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
      Paths: "Paths",
      Topics: "Topics",
      Mainlines: "Mainlines",
      Languages: "Language",
      PleaseChooseTopic: "Please choose topic",
      TopicsList: "Topics List",
      Reset: "Reset",
      SearchFromTopics: "Search from {topic_count} topics",
      ICP_MESSAGE: "ICP 2022148128",
      TopicStatisticsFormat: "{character_count} topics / {relation_count} relations / {group_count} groups",
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
      ShowTitle: "Show Title",
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
      ChooseCharacter: "Choose Character",
      Character: "Character",
      CharacterList: "Character List",
      AssociatedCharacters: "Associated Characters",
      Upstream: "Upstream",
      Downstream: "Downstream",
      Relation: "Relation",
      ImageName: "Image name",
      // Mainlines
      RelatedCharacters: "Related Characters",
      // Paths
      ComputePaths: "Compute Paths",
      SourceUser: "SourceUser",
      TargetUser: "TargetUser",
      OnlyDirected: "OnlyDirected",
      CutoffDegree: "CutoffDegree",
      Compute: "Compute",
      // Topics
      ManageTopics: "Manage Topics",
      TopicName: "Topic Name",
      CreateTopic: "Create Topic",
      DeleteTopic: "Delete Topic",
      SetOfficialTopic: "Set Official Topic",
      ExportDirectory: "Export Directory",
      ExportTopic: "Export Topic",
      ImportDirectory: "Import Directory",
      ImportTopic: "Import Topic",
      Official: "Official",
      NotOfficial: "Not Official",
      ExportAllTopic: "Export All Topic",
      importAllTopic: "import All Topic",
      // Edit
      AddCharacterWizard: "Add Character Wizard",
      EditAllCharacters: "Edit All Characters",
      EditAllRelations: "Edit All Relations",
      EditAllGroups: "Edit All Groups",
      EditAllMainlines: "Edit All Mainlines",
      WizardToAddNewCharacter: "Wizard to add new character",
      CreateCharacter: "Create Character",
      AddRelations: "Add Relations",
      JoinGroups: "Join Groups",
      UploadImage: "Upload Image",
      Submit: "Submit",
      NextStep: "Next Step",
      PreviousStep: "Previous Step",
      AddUpstreamRelation: "Add Upstream Relation",
      AddDownstreamRelation: "Add Downstream Relation",
      UpstreamCharacter: "Upstream Character",
      DownstreamCharacter: "Downstream Character",
      JoinGroup: "Join Group",
      Group: "Group",
      Done: "Done",  
      UpdateCharactersWeights: "Update Characters Weights",
      Algorithm: "Algorithm",
      CharactersTable: "Characters Table",
      AddRelation: "Add Relation",
      RelationsTable: "Relations Table",
      CreateGroup: "Create group",
      GroupName: "Group Name",
      AddToGroup: "Add To Group",
      GroupsTable: "Groups Table",
      AddMainlineEvent: "Add Mainline Event",
      BranchName: "Branch name",
      EventName: "Event name",
      PreviousEvent: "Previous event",
      FinalEvent: "Final event",
      MainlinesTable: "Mainlines Table"
    }
  },
  简体中文: {
    message: {
      // Home
      Home: '首页',
      Graph: '关系图',
      Characters: "角色",
      Edit: "编辑",
      Paths: "路径",
      Topics: "主题",
      Mainlines: "主线",
      Languages: "语言",
      PleaseChooseTopic: "请选择主题",
      TopicsList: "主题列表",
      Reset: "重置",
      SearchFromTopics: "从 {topic_count} 个主题中搜索",
      ICP_MESSAGE: "粤ICP备2022148128号",
      TopicStatisticsFormat: "{character_count} 角色 / {relation_count} 关系 / {group_count} 分组",
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
      ShowTitle: "显示标题",
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
      ChooseCharacter: "选择角色",
      Character: "角色",
      CharacterList: "角色列表",
      AssociatedCharacters: "关联角色",
      Upstream: "上游",
      Downstream: "下游",
      Relation: "关系",
      ImageName: "图片名",
      // Mainlines
      RelatedCharacters: "相关角色",
      // Paths
      ComputePaths: "计算路径",
      SourceUser: "源用户",
      TargetUser: "目标用户",
      OnlyDirected: "只包含有向图",
      CutoffDegree: "截止度",
      Compute: "计算",
      // Topics
      ManageTopics: "管理主题",
      TopicName: "主题名字",
      CreateTopic: "创建主题",
      DeleteTopic: "删除主题",
      SetOfficialTopic: "设置官方主题",
      ExportDirectory: "导出目录",
      ExportTopic: "导出主题",
      ImportDirectory: "导入目录",
      ImportTopic: "导入主题",
      Official: "官方",
      NotOfficial: "非官方",
      ExportAllTopic: "导出所有主题",
      importAllTopic: "导入所有主题",      
      // Edit
      AddCharacterWizard: "添加角色向导",
      EditAllCharacters: "编辑所有角色",
      EditAllRelations: "编辑所有关系",
      EditAllGroups: "编辑所有分组",
      EditAllMainlines: "编辑所有主线",
      WizardToAddNewCharacter: "添加新角色向导",
      CreateCharacter: "创建角色",
      AddRelations: "添加关系",
      JoinGroups: "加入分组",
      UploadImage: "上传图片",
      Submit: "提交",
      NextStep: "下一步",
      PreviousStep: "上一步",
      AddUpstreamRelation: "添加上游关系",
      AddDownstreamRelation: "添加下游关系",
      UpstreamCharacter: "上游角色",
      DownstreamCharacter: "下游角色",
      JoinGroup: "加入分组",
      Group: "分组",
      Done: "完成",
      UpdateCharactersWeights: "更新角色权重",
      Algorithm: "算法",
      CharactersTable: "角色表格",
      AddRelation: "添加关系",
      RelationsTable: "关系表格",
      CreateGroup: "创建分组",
      GroupName: "分组名字",
      AddToGroup: "添加到分组",
      GroupsTable: "分组表格",
      AddMainlineEvent: "添加主线事件",
      BranchName: "主线名",
      EventName: "事件名",
      PreviousEvent: "前置事件",
      FinalEvent: "最终事件",
      MainlinesTable: "主线表格"
    }
  },
  繁體中文: {
    message: {
      // Home
      Home: '首頁',
      Graph: '關係圖',
      Characters: "角色",
      Edit: "編輯",
      Paths: "路徑",
      Topics: "主題",
      Mainlines: "主線",
      Languages: "語言",
      PleaseChooseTopic: "請選擇主題",
      TopicsList: "主題列表",
      Reset: "重置",
      SearchFromTopics: "從 {topic_count} 個主題中搜索",
      ICP_MESSAGE: "粤ICP備2022148128號",
      TopicStatisticsFormat: "{character_count} 角色 / {relation_count} 關係 / {group_count} 分組",
      // Graph
      Groups: "分組",
      GraphAnimation: "關係圖動畫",
      Play: "播放",
      Stop: "暂停",
      GraphParameters: "關係圖參數",
      ChooseAll: "選擇全部",
      Name: "名字",
      Weight: "權重",
      Note: "備註",
      ShowTitle: "顯示標題",
      ImageMode: "圖片模式",
      RoamScaleMode: "ROAM縮放模式",
      CharactrWeightMode: "角色權重模式",
      CharactrSize: "角色大小",
      CharacterFontSize: "角色字體大小",
      RelationFontSize: "關係字體大小",
      ShadowSize: "陰影大小",
      LineWidth: "線寬",
      LineCurveness: "線曲度",
      // Characters
      ChooseCharacter: "選擇角色",
      Character: "角色",
      CharacterList: "角色列表",
      AssociatedCharacters: "關聯角色",
      Upstream: "上游",
      Downstream: "下游",
      Relation: "關係",
      ImageName: "圖片名",
      // Mainlines
      RelatedCharacters: "相關角色",      
      // Paths
      ComputePaths: "計算路徑",
      SourceUser: "源用户",
      TargetUser: "目標用户",
      OnlyDirected: "只包含有向圖",
      CutoffDegree: "截止度",
      Compute: "計算",
      // Topics
      ManageTopics: "管理主題",
      TopicName: "主題名字",
      CreateTopic: "創建主題",
      DeleteTopic: "刪除主題",
      SetOfficialTopic: "設置官方主題",
      ExportDirectory: "導出目錄",
      ExportTopic: "導入主題",
      ImportDirectory: "導入目錄",
      ImportTopic: "導入主題",
      Official: "官方",
      NotOfficial: "非官方",
      ExportAllTopic: "導出所有主題",
      importAllTopic: "導入所有主題",      
      // Edit
      AddCharacterWizard: "添加角色嚮導",
      EditAllCharacters: "編輯所有角色",
      EditAllRelations: "編輯所有關係",
      EditAllGroups: "編輯所有分組",
      EditAllMainlines: "編輯所有主線",
      WizardToAddNewCharacter: "添加新角色嚮導",
      CreateCharacter: "創建角色",
      AddRelations: "添加關係",
      JoinGroups: "加入分組",
      UploadImage: "上傳圖片",
      Submit: "提交",
      NextStep: "下一步",
      PreviousStep: "上一步",
      AddUpstreamRelation: "添加上游關係",
      AddDownstreamRelation: "添加下游關係",
      UpstreamCharacter: "上游角色",
      DownstreamCharacter: "下游角色",
      JoinGroup: "加入分組",
      Group: "分組",
      Done: "完成",
      UpdateCharactersWeights: "更新角色權重",
      Algorithm: "算法",
      CharactersTable: "角色表格",
      AddRelation: "添加關係",
      RelationsTable: "關係表格",
      CreateGroup: "創建分組",
      GroupName: "分組名字",
      AddToGroup: "添加到分組",
      GroupsTable: "分組表格",
      AddMainlineEvent: "添加主線事件",
      BranchName: "主線名",
      EventName: "事件名",
      PreviousEvent: "前置事件",
      FinalEvent: "最終事件",
      MainlinesTable: "主線表格"
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
