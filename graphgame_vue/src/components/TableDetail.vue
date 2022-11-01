
<template>
  <h1>TableDetail</h1>

  <vxe-grid ref="nodesGridTable" v-bind="nodesTableOptions" v-on="nodesTableEvents">
    <template #id_edit="{ row }">
      <vxe-input v-model="row.id"></vxe-input>
    </template>
    <template #name_edit="{ row }">
      <vxe-input v-model="row.name"></vxe-input>
    </template>
    <template #display_name_edit="{ row }">
      <vxe-input v-model="row.display_name"></vxe-input>
    </template>
    <template #note_edit="{ row }">
      <vxe-input v-model="row.note"></vxe-input>
    </template>
    <template #weight_edit="{ row }">
      <vxe-input v-model="row.weight"></vxe-input>
    </template>
  </vxe-grid>


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

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'
import { VXETable, VxeGridInstance, VxeGridListeners, VxeGridProps } from 'vxe-table'

export default defineComponent({
  name: "TableDetail",
  props: {
    page_name: String,
  },
  setup () {
    const dbName = ref("cyberpunk_edgerunner");
    let nodes = ref([]);
    let edges = ref([]);
    let groups = ref([]);



    const nodesGridTable = ref<VxeGridInstance>()
    const nodesTableOptions = reactive<VxeGridProps>({
      border: true,
      keepSource: true,
      id: 'toolbar_demo_1',
      height: 530,
      printConfig: {},
      importConfig: {},
      exportConfig: {},
      columnConfig: {
        resizable: true
      },
      customConfig: {
        storage: true
      },
      editConfig: {
        trigger: 'click',
        mode: 'row',
        showStatus: true
      },
      columns: [
        { field: 'id', title: 'Id', slots: { edit: 'id_edit' } },
        { field: 'name', title: 'Name', slots: { edit: 'name_edit' } },
        { field: 'display_name', title: 'Display Name', slots: { edit: 'display_name_edit' } },
        { field: 'note', title: 'Note', slots: { edit: 'note_edit' } },
        { field: 'weight', title: 'Weight', slots: { edit: 'weight_edit' } }
      ],
      toolbarConfig: {
        buttons: [
          { code: 'myInsert', name: 'New', status: 'primary' },
          { code: 'mySave', name: 'Save', status: 'success' },
        ],
        import: true,
        export: true,
        zoom: true,
        custom: true
      },
      /*
      data: [
      {
        "display_name": "David Martinez", 
        "name": "david", 
        "weight": 0.238291
      }, 
      {
        "display_name": "Lucy", 
        "name": "lucy", 
        "weight": 0.123158
      }]*/
      data: []
    })

    const nodesTableEvents: VxeGridListeners = {
      toolbarButtonClick ({ code }) {
        const $grid = nodesGridTable.value
        switch (code) {
          case 'myInsert': {
            $grid.insert({
              
            })
            break
          }
          case 'mySave': {
            const { insertRecords, removeRecords, updateRecords } = $grid.getRecordset()
            VXETable.modal.message({ content: `新增 ${insertRecords.length} 条，删除 ${removeRecords.length} 条，更新 ${updateRecords.length} 条`, status: 'success' })
            break
          }
          case 'myExport': {
            $grid.exportData({
              type: 'csv'
            })
            break
          }
        }
      },
      toolbarToolClick ({ code }) {
        const $grid = nodesGridTable.value
        switch (code) {
          case 'myPrint': {
            $grid.print()
            break
          }
        }
      }
    }


    onMounted(() => {

      axios.get(`http://127.0.0.1:7788/api/${dbName.value}/nodes`)
        .then(response => {
          nodes.value = response.data.nodes;

          nodesTableOptions.data = response.data.nodes;
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
      groups,
      nodesGridTable,
      nodesTableOptions,
      nodesTableEvents
    }
  }
})
</script>

<style scoped>
</style>