
<template>

  <a-row>

    <a-col :span="12">


      <h1>Topics</h1>

      <a-list item-layout="horizontal" :data-source="topics">
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta
              description="10 characters / 50 relations / 2 groups"
            >
              <template #title>
                <router-link :to='`/topics/${item}/graph`'>{{ item }}</router-link>

              </template>

              <template #avatar>
                <a @click="previewGraph(item)">
                  <a-avatar src="/gb_logo.png" />
                </a>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
      </a-list>

    </a-col>

    <a-col :span="12">
      <div v-if="chosenTopicName">
        <GraphDetail :topic="chosenTopicName" :only-graph=true></GraphDetail>
      </div>
    </a-col>
  </a-row>

</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import type { UnwrapRef } from 'vue';

import GraphDetail from './GraphDetail.vue';

export default defineComponent({
  name: "TopicList",
  props: {},
  components: {
    GraphDetail
  },
  setup() {

    const topics = ref([]);
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
      axios.get(`http://127.0.0.1:7788/api/topics`)
        .then(response => {
          topics.value = response.data.topics;

          // Select the random topic to display by default
          const randomIndex = getRandomInt(0, response.data.topics.length - 1);
          chosenTopicName.value = response.data.topics[randomIndex];
        })
        .catch(error => {
          console.log(error);
        });
    }


    onMounted(() => {
      initTopicListData();
    })

    return {
      topics,
      chosenTopicName,
      previewGraph
    }
  }
})
</script>
