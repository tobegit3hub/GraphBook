
<template>

  <h2>Edit characters:</h2>
  <NodesTable :db-name="dbName"></NodesTable>

  <h2>Edit relations:</h2>
  <EdgesTable :db-name="dbName"></EdgesTable>

  <h2>Edit groups:</h2>
  <GroupsTable :db-name="dbName"></GroupsTable>

</template>

<script>
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'

import NodesTable from './NodesTable.vue';
import EdgesTable from './EdgesTable.vue';
import GroupsTable from './GroupsTable.vue';

export default defineComponent({
  name: "EditGraph",
  props: {
    dbName: String,
  },
  setup (props) {
   
    return {

    }
  }
})
</script>
