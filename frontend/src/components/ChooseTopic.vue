
<template>

  <div style="padding: 20px">

    <a-result status="warning" :title="$t('message.PleaseChooseTopic')">
      <template #extra>
      </template>
    </a-result>

    <!-- List of all topics -->
    <all-topic-list></all-topic-list>

  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import AllTopicList from './AllTopicList.vue';

export default defineComponent({
  name: "ChooseTopic",
  props: {},
  components: {
    AllTopicList
  },
  setup() {
    return {
    }
  }
})
</script>
