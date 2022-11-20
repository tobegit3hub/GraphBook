
<template>

<a-select
    v-model:value="value"
    show-search
    placeholder="Select a person"
    style="width: 200px"
    :options="options"
    :filter-option="filterOption"
    @focus="handleFocus"
    @blur="handleBlur"
    @change="handleChange"
  ></a-select>

  <vxe-grid ref="vxeTable" v-bind="vxeTableOptions" v-on="vxeTableHandler">
    <template #name_edit="{ row }">
      <vxe-input v-model="row.name"></vxe-input>
    </template>
    <template #character_name_edit="{ row }">
      <vxe-input v-model="row.character_name"></vxe-input>
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
import type { SelectProps } from 'ant-design-vue';

type SelectItem = {
  value: string;
  label: string;
};

export default defineComponent({
  name: "GroupsTable",
  props: {
    topic: String,
  },
  setup (props) {
    const vxeTable = ref<VxeGridInstance>()
    const vxeTableOptions = reactive<VxeGridProps>({
      border: true,
      keepSource: true,
      id: 'groups_table',
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
        { field: 'name', title: 'Group Name', editRender: {}, slots: { edit: 'name_edit' } },
        { field: 'character_name', title: 'Character Name', editRender: {}, slots: { edit: 'character_name_edit' } },
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

            axios.post(`http://127.0.0.1:7788/api/topics/${props.topic}/groups`, {
              insert_groups: insertRecords,
              update_groups: updateRecords,
              delete_groups: removeRecords
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


    const options = ref<SelectProps['options']>([
      { value: 'jack', label: 'Jack' },
      { value: 'lucy', label: 'Lucy' },
      { value: 'tom', label: 'Tom' },
    ]);
    const handleChange = (value: string) => {
      console.log(`selected ${value}`);
    };
    const handleBlur = () => {
      console.log('blur');
    };
    const handleFocus = () => {
      console.log('focus');
    };
    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    onMounted(() => {
      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/groups`)
        .then(response => {
          vxeTableOptions.data = response.data.groups;
        })
        .catch(error => {
          console.log(error);
        });

        axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/characters`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.characters.forEach(character => {
            selectItems.push({"value": character.name, "label": character.name})
          });
          options.value = [...selectItems];
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

      value: ref<string | undefined>(undefined),
      filterOption,
      handleBlur,
      handleFocus,
      handleChange,
      options,
    }
  }
})
</script>
