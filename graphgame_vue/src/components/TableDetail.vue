
<template>
  <h1>TableDetail</h1>

  <vxe-grid ref="nodesGridTable" v-bind="nodesTableOptions" v-on="nodesTableEvents">

    <template #operate="{ row }">
      <vxe-button title="Delete" circle @click="removeNode(row)" status="danger"></vxe-button>
    </template>

    <template #id_edit="{ row }">
      <vxe-input v-model="row.row_id"></vxe-input>
    </template>
    <template #name_edit="{ row }">
      <vxe-input v-model="row.name"></vxe-input>
    </template>
    <template #display_name_edit="{ row }">
      <vxe-input v-model="row.display_name"></vxe-input>
    </template>
    <template #note_edit="{ row }">
      <vxe-textarea v-model="row.note" :autosize="{ minRows: 1, maxRows: 8 }"></vxe-textarea>
    </template>
    <template #weight_edit="{ row }">
      <vxe-input v-model="row.weight"></vxe-input>
    </template>
  </vxe-grid>


  <h2>Nodes:</h2>
  <vxe-table border :data="nodes">
    <vxe-column field="row_id" title="Id"></vxe-column>
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
    dbName: String,
  },
  setup (props) {
    let nodes = ref([]);
    let edges = ref([]);
    let groups = ref([]);

    const nodesGridTable = ref<VxeGridInstance>()
    const nodesTableOptions = reactive<VxeGridProps>({
      border: true,
      keepSource: true,
      id: 'node_table',
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
        { field: 'row_id', title: 'Id', slots: { edit: 'id_edit' } },
        { field: 'name', title: 'Name', editRender: {}, slots: { edit: 'name_edit' } },
        { field: 'display_name', title: 'Display Name', editRender: {}, slots: { edit: 'display_name_edit' } },
        { field: 'note', title: 'Note', editRender: {}, slots: { edit: 'note_edit' } },
        { field: 'weight', title: 'Weight', slots: { edit: 'weight_edit' } },
        { title: 'Delete', width: 200, slots: { default: 'operate' } }
      ],
      toolbarConfig: {
        buttons: [
          { code: 'insertButton', name: 'New', status: 'primary' },
          { code: 'saveButton', name: 'Save', status: 'success' }
        ],
        import: false, // TODO: Support and test
        export: true,
        zoom: true,
        custom: true,
        refresh: false
      },
      data: []
    })

    const nodesTableEvents: VxeGridListeners = {
      toolbarButtonClick ({ code }) {
        const $grid = nodesGridTable.value
        switch (code) {
          case 'insertButton': {
            $grid.insert({
            })
            break
          }
          case 'saveButton': {
            const { insertRecords, removeRecords, updateRecords } = $grid.getRecordset()
            VXETable.modal.message({ content: `Add ${insertRecords.length} rows, delete ${removeRecords.length} rows, update ${updateRecords.length} rows`, status: 'success' })

            axios.post(`http://127.0.0.1:7788/api/${props.dbName}/nodes`, {
              insert_nodes: insertRecords,
              update_nodes: updateRecords,
              delete_nodes: removeRecords
            })
            .then(function (response) {
              console.log(response);
            })
            .catch(function (error) {
              console.log(error);
            });

            break
          }
          case 'saveButton': {

          }
        }
      }
    }

    onMounted(() => {

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/nodes`)
        .then(response => {
          nodes.value = response.data.nodes;

          nodesTableOptions.data = response.data.nodes;
        })
        .catch(error => {
          console.log(error);
        });

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/edges`)
        .then(response => {
          edges.value = response.data.edges;
        })
        .catch(error => {
          console.log(error);
        });

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/groups`)
        .then(response => {
          groups.value = response.data.groups;
        })
        .catch(error => {
          console.log(error);
        });
    })

    const removeNode = async (row: any) => {
      const type = await VXETable.modal.confirm("Are you sure to delete?")
      const $grid = nodesGridTable.value
      if ($grid) {
        if (type === 'confirm') {
          await $grid.remove(row)
        }
      }
    }


    return {
      nodes,
      edges,
      groups,
      nodesGridTable,
      nodesTableOptions,
      nodesTableEvents,
      removeNode
    }
  }
})
</script>

<style scoped>
</style>