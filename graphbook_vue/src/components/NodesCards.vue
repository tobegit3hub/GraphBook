
<template>

<div style="background-color: #ececec; padding: 20px">
    <a-row :gutter="16">


      <div v-for="node in nodes">
     
        <a-col :span="4">
          <a-card hoverable style="width: 240px">
          <template #cover>
            <img :src="'http://localhost:7788/images/' + dbName + '/' + node.name + '.png'" />
          </template>
          <a-card-meta :title="node.display_name">
            <template #description>{{ node.note }}</template>
          </a-card-meta>
        </a-card>
        </a-col>

      </div>


    </a-row>
  </div>


</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'
import { VXETable, VxeGridInstance, VxeGridListeners, VxeGridProps } from 'vxe-table'

export default defineComponent({
  name: "NodesCard",
  props: {
    dbName: String,
  },
  setup (props) {
   
    let nodes = ref([]);

    onMounted(() => {
      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/nodes`)
        .then(response => {
          nodes.value = response.data.nodes;
        })
        .catch(error => {
          console.log(error);
        });
    })

    return {
      nodes
    }
  }
})
</script>
