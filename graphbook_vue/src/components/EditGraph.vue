
<template>

  <h2>Update weights:</h2>
  <a-button type="primary" @click="updateCharactersWeights">Update with PageRank</a-button>

  <h2>Edit characters:</h2>
  <CharactersTable :topic="topic"></CharactersTable>

  <h2>Edit relations:</h2>
  <RelationsTable :topic="topic"></RelationsTable>

  <h2>Edit groups:</h2>
  <GroupsTable :topic="topic"></GroupsTable>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'
import { message } from 'ant-design-vue';

import CharactersTable from './CharactersTable.vue';
import RelationsTable from './RelationsTable.vue';
import GroupsTable from './GroupsTable.vue';

export default defineComponent({
  name: "EditGraph",
  props: {
    topic: String,
  },
  setup (props) {

    const updateCharactersWeights = () => {
      axios.put(`http://127.0.0.1:7788/api/topics/${props.topic}/weights`)
        .then(function (response) {
          // TODO: ant css is lost
          message.success('Success to update characters weights');
        })
        .catch(function (error) {
          message.error('Fail to update characters weights, ' + error);
        });
    }
   
    return {
      updateCharactersWeights
    }
  }
})
</script>
