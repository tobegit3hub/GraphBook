
<template>

  <h1>Add realtion</h1>
  <a-form
      layout="inline"
      :model="formState"
      @finish="handleSubmitForm"
      @finishFailed="handleSubmitFormFailed"
    >

  <a-form-item>
      <a-select
        v-model:value="formState.source"
        show-search
        placeholder="Select character"
        style="width: 200px"
        :options="selectCharacterOptions"
        :filter-option="filterOption"
      ></a-select>
    </a-form-item>

    <a-form-item>
      <a-select
        v-model:value="formState.target"
        show-search
        placeholder="Select character"
        style="width: 200px"
        :options="selectCharacterOptions"
        :filter-option="filterOption"
      ></a-select>
    </a-form-item>

    <a-form-item
      label="relation"
      name="relation"
      :rules="[{ required: true, message: 'Please input relation!' }]"
    >
      <a-input v-model:value="formState.relation" />
    </a-form-item>

    <a-form-item
      label="note"
      name="note"
    >
      <a-input v-model:value="formState.note" />
    </a-form-item>

    <a-form-item>
      <a-button
        type="primary"
        html-type="submit"
        :disabled="formState.source === '' || formState.target === '' || formState.relation === ''"
      >
        Add
      </a-button>
    </a-form-item>
  </a-form>

  <br /><br />

  <h1>Relations table</h1>
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
import type { UnwrapRef } from 'vue';
import { VXETable, VxeGridInstance, VxeGridListeners, VxeGridProps } from 'vxe-table'
import type { SelectProps, FormProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';

type SelectItem = {
  value: string;
  label: string;
};

interface FormState {
  source: string;
  target: string;
  relation: string;
  note: string;
}

export default defineComponent({
  name: "EditRelations",
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

            axios.post(`/api/topics/${props.topic}/relations`, {
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

    const formState: UnwrapRef<FormState> = reactive({
      source: '',
      target: '',
      relation: '',
      note: ''
    });
    
    const handleSubmitForm: FormProps['onFinish'] = values => {

      axios.post(`/api/topics/${props.topic}/relations`, {
          "source": formState.source,
          "target": formState.target,
          "relation": formState.relation,
          "note": formState.note
        })
        .then(response => {
          message.success(`Success to add source: ${formState.source} to target ${formState.target}`);
          initTableData();
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleSubmitFormFailed: FormProps['onFinishFailed'] = errors => {
      console.log("Fail to submit form: " + errors);
    };

    const selectCharacterOptions = ref<SelectProps['options']>([]);

    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const initTableData = () => {
      axios.get(`/api/topics/${props.topic}/relations`)
        .then(response => {
          vxeTableOptions.data = response.data.relations;
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      initTableData();

      axios.get(`/api/topics/${props.topic}/characters`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.characters.forEach(character => {
            selectItems.push({"value": character.name, "label": character.name})
          });
          selectCharacterOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
      });        
    })

    return {
      vxeTable,
      vxeTableOptions,
      vxeTableHandler,
      removeRow,

      formState,
      handleSubmitForm,
      handleSubmitFormFailed,

      filterOption,
      selectCharacterOptions
    }
  }
})
</script>
