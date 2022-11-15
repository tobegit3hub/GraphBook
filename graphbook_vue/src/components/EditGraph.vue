
<template>

  <h2>Edit characters:</h2>
  <CharactersTable :topic="topic"></CharactersTable>

  <h2>Edit relations:</h2>
  <RelationsTable :topic="topic"></RelationsTable>

  <h2>Edit groups:</h2>
  <GroupsTable :topic="topic"></GroupsTable>

</template>

<script>
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'

import CharactersTable from './CharactersTable.vue';
import RelationsTable from './RelationsTable.vue';
import GroupsTable from './GroupsTable.vue';

export default defineComponent({
  name: "EditGraph",
  props: {
    topic: String,
  },
  setup (props) {
   
    return {

    }
  }
})
</script>
