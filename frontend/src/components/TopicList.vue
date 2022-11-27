
<template>

  <a-row>

    <a-col :span="8">

      <br />
      <h1>Topics</h1>

      <a-list item-layout="horizontal" :data-source="topicsListData">
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta :description="item.statistic_string">
              <template #title>
                <router-link :to='`/topics/${item.name}/graph`'>{{ item.name }}</router-link>
              </template>

              <template #avatar>
                <a @click="previewGraph(item.name)">
                  <a-avatar src="/gb_logo.png" />
                </a>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
      </a-list>

    </a-col>

    <a-col :span="16">
      <div v-if="chosenTopicName">
        <GraphDetail :topic="chosenTopicName" :only-graph=true></GraphDetail>
      </div>
    </a-col>
  </a-row>

</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import axios from 'axios'

import GraphDetail from './GraphDetail.vue';

interface TopicsListItem {
  name: string;
  statistic_string: string
}

export default defineComponent({
  name: "TopicList",
  props: {},
  components: {
    GraphDetail
  },
  setup() {
    const topicsListData = reactive<TopicsListItem[]>([]);
    const chosenTopicName = ref("");

    const previewGraph = (name) => {
      chosenTopicName.value = name;
    }

    const getRandomInt = (min, max) => {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    const initTopicListData = () => {

      axios.get(`/api/topics_statistics`)
        .then(response => {
          const topic_count = response.data.count;

          response.data.statistics.forEach((statistic) => {
            const statistic_string = `${statistic.characters} characters / ${statistic.relations} relations / ${statistic.groups} groups`
            topicsListData.push({ name: statistic.topic, statistic_string: statistic_string })
          });

          // Select the random topic to display by default
          const randomIndex = getRandomInt(0, topic_count - 1);
          chosenTopicName.value = response.data.statistics[randomIndex].topic
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      initTopicListData();
    })

    return {
      topicsListData,
      chosenTopicName,
      previewGraph
    }
  }
})
</script>
