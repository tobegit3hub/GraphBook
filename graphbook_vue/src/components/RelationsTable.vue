
<template>

  <vxe-grid ref="vxeTable" v-bind="vxeTableOptions" v-on="vxeTableHandler">
    <template #source_edit="{ row }">
      <vxe-input v-model="row.source"></vxe-input>
    </template>
    <template #target_edit="{ row }">
      <vxe-input v-model="row.target"></vxe-input>
    </template>
    <template #relation_edit="{ row }">
      <vxe-input v-model="row.relation"></vxe-input>
    </template>
    <template #note_edit="{ row }">
      <vxe-textarea v-model="row.note" :autosize="{ minRows: 1, maxRows: 8 }"></vxe-textarea>
    </template>

    <template #operate="{ row }" slot-scope="scope">
      <!-- TODO: icon is not displayed -->
      <vxe-button @click="removeRow(row)" circle status="warning" icon="fa fa-trash-o"></vxe-button>
    </template>
  </vxe-grid>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'
import { VXETable, VxeGridInstance, VxeGridListeners, VxeGridProps } from 'vxe-table'

export default defineComponent({
  name: "RelatioinsTable",
  props: {
    topic: String,
  },
  setup (props) {
    const vxeTable = ref<VxeGridInstance>()
    const vxeTableOptions = reactive<VxeGridProps>({
      border: true,
      keepSource: true,
      id: 'relations_table',
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
        { field: 'source', title: 'Source', editRender: {}, slots: { edit: 'source_edit' } },
        { field: 'target', title: 'Target', editRender: {}, slots: { edit: 'target_edit' } },
        { field: 'relation', title: 'Relation', editRender: {}, slots: { edit: 'relation_edit' } },
        { field: 'note', title: 'Note', editRender: {}, slots: { edit: 'note_edit' } },
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

    const vxeTableHandler: VxeGridListeners = {
      toolbarButtonClick ({ code }) {
        const $grid = vxeTable.value
        switch (code) {
          case 'insertButton': {
            $grid.insert({
            })
            break
          }
          case 'saveButton': {
            const { insertRecords, removeRecords, updateRecords } = $grid.getRecordset()
            VXETable.modal.message({ content: `Add ${insertRecords.length} rows, update ${updateRecords.length} rows, delete ${removeRecords.length} rows`, status: 'success' })

            axios.post(`http://127.0.0.1:7788/api/topics/${props.topic}/relations`, {
              insert_relations: insertRecords,
              update_relations: updateRecords,
              delete_relations: removeRecords
            })
            .then(function (response) {
              console.log(response);
            })
            .catch(function (error) {
              console.log(error);
            });
            break
          }
        }
      }
    }

    const removeRow = async (row: any) => {
      const type = await VXETable.modal.confirm("Are you sure to delete?")
      const $grid = vxeTable.value
      if ($grid) {
        if (type === 'confirm') {
          await $grid.remove(row)
        }
      }
    }

    onMounted(() => {
      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/relations`)
        .then(response => {
          vxeTableOptions.data = response.data.relations;
        })
        .catch(error => {
          console.log(error);
        });
    })

    return {
      vxeTable,
      vxeTableOptions,
      vxeTableHandler,
      removeRow
    }
  }
})
</script>
