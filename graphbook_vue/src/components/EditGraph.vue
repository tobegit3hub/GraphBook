
<template>

  <h2>Update weights:</h2>
  <a-button type="primary" @click="updateCharactersWeights">Update with PageRank</a-button>


  <h2>Edit characters:</h2>
  <EditCharacters :topic="topic"></EditCharacters>

  <h2>Edit relations:</h2>
  <EditRelations :topic="topic"></EditRelations>

  <h2>Edit groups:</h2>
  <EditGroups :topic="topic"></EditGroups>


</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'
import { message } from 'ant-design-vue';

import CharactersTable from './EditCharacters.vue';
import EditRelations from './EditRelations.vue';
import EditGroups from './EditGroups.vue';

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
