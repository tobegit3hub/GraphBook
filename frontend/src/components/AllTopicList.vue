
<template>

  <!-- List of all topics -->
  <h1> {{ $t('TopicsList') }}</h1>

  <a-list item-layout="horizontal" :data-source="topics">
    <template #renderItem="{ item }">
      <a-list-item>          
        <router-link :to='`/topics/${item.name}`'>
          {{ item.name }}
          <!-- Show official icon if it is -->
          <span v-show="(item.official == 1)">
            &nbsp;<img src="/verified_icon.png" width="10" />
          </span>
        </router-link>
      </a-list-item>
    </template>
  </a-list>

</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: "AllTopicList",
  setup() {
    const topics = ref([]);

    const init = () => {
      axios.get(`/api/topics`)
        .then(response => {
          topics.value = response.data.topics;
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      init();
    })

    return {
      topics
    }
  }
})
</script>
