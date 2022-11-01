
<template>
  <h1>TableDetail</h1>

  <h2>Nodes:</h2>
  <vxe-table border :data="nodes">
    <vxe-column field="id" title="Id"></vxe-column>
    <vxe-column field="name" title="Name"></vxe-column>
    <vxe-column field="display_name" title="Display Name"></vxe-column>
    <vxe-column field="note" title="Note"></vxe-column>
    <vxe-column field="weight" title="Weight"></vxe-column>
  </vxe-table>

  <h2>Edges:</h2>
  <vxe-table border :data="edges">
    <vxe-column field="id" title="Id"></vxe-column>
    <vxe-column field="source" title="Source"></vxe-column>
    <vxe-column field="target" title="Target"></vxe-column>
    <vxe-column field="relation" title="Relation"></vxe-column>
  </vxe-table>

  <h2>Groups:</h2>
  <vxe-table border :data="groups">
    <vxe-column field="id" title="Id"></vxe-column>
    <vxe-column field="name" title="Group Name"></vxe-column>
    <vxe-column field="node_name" title="Node Name"></vxe-column>
  </vxe-table>
</template>

<script>
import { ref, onMounted} from 'vue'

import axios from 'axios'

export default {
  name: "TableDetail",
  setup () {
    const dbName = ref("cyberpunk_edgerunner");
    let nodes = ref([]);
    let edges = ref([]);
    let groups = ref([]);

    onMounted(() => {

      axios.get(`http://127.0.0.1:7788/api/${dbName.value}/nodes`)
        .then(response => {
          nodes.value = response.data.nodes;
        })
        .catch(error => {
          console.log(error);
        });

      axios.get(`http://127.0.0.1:7788/api/${dbName.value}/edges`)
        .then(response => {
          edges.value = response.data.edges;
        })
        .catch(error => {
          console.log(error);
        });

      axios.get(`http://127.0.0.1:7788/api/${dbName.value}/groups`)
        .then(response => {
          groups.value = response.data.groups;
        })
        .catch(error => {
          console.log(error);
        });
    })

    return {
      nodes,
      edges,
      groups
    }
  }
}
</script>

<style scoped>
</style>