
<template>

  <a-row>

    <a-col :span="8">

      <br />
      <h1>{{ $t('Topics') }}</h1>

      <a-select v-model:value="selectTopicName" show-search :placeholder="$t('SearchFromTopics', {topic_count: topic_count})"
        style="width: 250px" :options="selectTopicOptions" @change="changeSelectTopic">
      </a-select>
      <a-button @click="resetSelectTopic">{{ $t('Reset') }}</a-button>

      <br /><br />
      <a-list item-layout="horizontal" :data-source="topicsListData">
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta :description="$t('TopicStatisticsFormat', {character_count: item.character_count, relation_count: item.relation_count, group_count: item.group_count})">
              <template #title>
                <router-link :to='`/topics/${item.name}`'>
                  {{ item.name }}
                  <span v-show="item.official">
                    &nbsp;<img src="/verified_icon.png" width="10" />
                  </span>
                </router-link>

              </template>

              <template #avatar>
                <a @click="previewGraph(item.name)">
                  <a-avatar src="/topicland_logo.png" />
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
import { SelectTypes } from 'ant-design-vue/es/select';

import GraphDetail from './GraphDetail.vue';

type SelectItem = {
  value: string;
  label: string;
};

interface TopicsListItem {
  name: string;
  official: boolean;
  character_count: number;
  relation_count: number;
  group_count: number;
}

export default defineComponent({
  name: "HomeTopicList",
  props: {},
  components: {
    GraphDetail
  },
  setup() {

    const selectTopicName = ref<string>();
    const selectTopicOptions = ref<SelectTypes['options']>([]);

    const changeSelectTopic = () => {
      previewGraph(selectTopicName.value);

      // Get one topic statistics to show
      axios.get(`/api/topics/statistics`, {
        params: {
          "topic_name": selectTopicName.value
        }
      })
        .then(response => {
          // Reset the array
          topicsListData.splice(0)

          topicsListData.push({ 
            name: response.data.topic,
            official: response.data.official,
            character_count: response.data.characters,
            relation_count: response.data.relations,
            group_count: response.data.groups
          })
        })
        .catch(error => {
          console.log(error);
        });
    }

    const topicsListData = reactive<TopicsListItem[]>([]);
    const chosenTopicName = ref("");
    const topic_count = ref();

    const resetSelectTopic = () => {
      selectTopicName.value = undefined;
      initTopicListData();
    }

    const previewGraph = (name) => {
      chosenTopicName.value = name;
    }

    const getRandomInt = (min, max) => {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    const init = () => {
      axios.get(`/api/topics/names`)
        .then(response => {
          topic_count.value = response.data.topics.length;

          const selectItems: SelectItem[] = [];
          // Set the options for select
          response.data.topics.forEach(topicName => {
            selectItems.push({ "value": topicName, "label": topicName })
          });
          selectTopicOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
        });

      initTopicListData();
    }

    const initTopicListData = () => {
      axios.get(`/api/topics/statistics`, {
        params: {
          count: 10
        }
      })
        .then(response => {
          const limited_topic_count = response.data.count;

          // Reset the array
          topicsListData.splice(0)

          // Get topic list and their statistics
          response.data.statistics.forEach((statistic) => {
            topicsListData.push({
              name: statistic.topic,
              official: statistic.official,
              character_count: statistic.characters,
              relation_count: statistic.relations,
              group_count: statistic.groups
            })
          });

          // Select the random topic to display by default
          const randomIndex = getRandomInt(0, limited_topic_count - 1);
          chosenTopicName.value = response.data.statistics[randomIndex].topic
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      init();
    })

    return {
      selectTopicName,
      selectTopicOptions,
      changeSelectTopic,
      topic_count,
      resetSelectTopic,

      topicsListData,
      chosenTopicName,
      previewGraph
    }
  }
})
</script>
