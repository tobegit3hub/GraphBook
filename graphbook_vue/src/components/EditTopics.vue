
<template>

  <div style="padding: 20px">
      <h1> Manage Topics</h1>

      <!-- Form to create topic -->
      <a-form layout="inline" :model="formState" @finish="handleCreateTopicFinish" @finishFailed="handleFinishFailed">
        <a-form-item>
          <a-input v-model:value="formState.name" placeholder="Topic name">
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">
            Create Topic
          </a-button>
        </a-form-item>
      </a-form>

      <br />
      <!-- Form to delete topic -->
      <a-form layout="inline" :model="deleteTopicFormState" @finish="handleDeleteTopicFinish" @finishFailed="handleFinishFailed">
        <a-form-item>
          <a-input v-model:value="deleteTopicFormState.name" placeholder="Topic name">
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">
            Delete Topic
          </a-button>
        </a-form-item>
      </a-form>

      <br /><br />
      <h1> Topics List</h1>
      <a-list item-layout="horizontal" :data-source="topics">
        <template #renderItem="{ item }">
          <a-list-item>
            <router-link :to='`/topics/${item}/graph`'>{{ item }}</router-link>
          </a-list-item>
        </template>
      </a-list>

  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import type { UnwrapRef } from 'vue';
import { useRouter, useRoute } from 'vue-router'
import type { FormProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';

import GraphDetail from './GraphDetail.vue';

interface FormState {
  name: string;
}

export default defineComponent({
  name: "EditTopics",
  props: {},
  components: {
    GraphDetail
  },
  setup() {

    const topics = ref([]);
    const chosenTopicName = ref("");

    const formState: UnwrapRef<FormState> = reactive({
      name: ''
    });

    const deleteTopicFormState: UnwrapRef<FormState> = reactive({
      name: ''
    });

    const handleCreateTopicFinish: FormProps['onFinish'] = values => {

      axios.post(`http://127.0.0.1:7788/api/topics`, {
          "name": formState.name
        })
        .then(response => {
          message.success('Success to create topic: ' + formState.name);
          initTopicListData()
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleDeleteTopicFinish: FormProps['onFinish'] = values => {

      axios.delete(`http://127.0.0.1:7788/api/topics/${deleteTopicFormState.name}`)
        .then(response => {
          message.success('Success to delete topic: ' + deleteTopicFormState.name);
          initTopicListData();
        })
        .catch(error => {
          console.log(error);
        });
      };

    const handleFinishFailed: FormProps['onFinishFailed'] = errors => {
      console.log(errors);
    };

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
      formState,
      handleCreateTopicFinish,

      deleteTopicFormState,
      handleDeleteTopicFinish,
      handleFinishFailed,
      previewGraph
    }
  }
})
</script>
