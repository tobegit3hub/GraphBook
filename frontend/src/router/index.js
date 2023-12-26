import { createRouter, createWebHashHistory } from 'vue-router'

//import App from './App.vue'
import HomeTopicList from '@/components/HomeTopicList.vue';
import GraphDetail from '@/components/GraphDetail.vue';
import ComputePaths from '@/components/ComputePaths.vue'
import GroupsList from '@/components/GroupsList.vue'
import GroupDetail from '@/components/GroupDetail.vue'
import ChooseCharacters from '@/components/ChooseCharacters.vue';
import CharacterDetail from '@/components/CharacterDetail.vue';
import EditTopics from '@/components/EditTopics.vue';
import EditGraph from '@/components/EditGraph.vue';
import AddCharacterWizard from '@/components/AddCharacterWizard.vue';
import EditCharacters from '@/components/EditCharacters.vue';
import EditRelations from '@/components/EditRelations.vue';
import EditGroups from '@/components/EditGroups.vue';
import EditMainlines from '@/components/EditMainlines.vue';
import ChooseTopic from '@/components/ChooseTopic.vue';
import MainlineDetail from '@/components/MainlineDetail.vue';

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

export default router