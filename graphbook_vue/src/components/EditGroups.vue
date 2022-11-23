
<template>

  <h1>Create group</h1>
  <a-input-group compact>
    <a-input v-model:value="createGroupName" style="width: calc(100% - 200px)" placeholder="group name" />
    <a-button type="primary" @click="handleCreateGroup">Create</a-button>
  </a-input-group>

  <br />

  <h1>Add to group</h1>
  <a-form
    layout="inline"
    :model="formState"
    @finish="handleSubmitForm"
    @finishFailed="handleSubmitFormFailed"
  >

  <a-form-item>
      <a-select
        v-model:value="formState.character_name"
        show-search
        placeholder="Select character"
        style="width: 200px"
        :options="selectCharacterOptions"
        :filter-option="filterOption"
      ></a-select>
    </a-form-item>

    <a-form-item>
      <a-select
        v-model:value="formState.group_name"
        show-search
        placeholder="Select group"
        style="width: 200px"
        :options="selectGroupOptions"
        :filter-option="filterOption"
      ></a-select>
    </a-form-item>

    <a-form-item>
      <a-button
        type="primary"
        html-type="submit"
        :disabled="formState.group_name === '' || formState.character_name === ''"
      >
        Add
      </a-button>
    </a-form-item>
  </a-form>

  <br /><br />

  <h1>Groups table</h1>
  <vxe-grid ref="vxeTable" v-bind="vxeTableOptions" v-on="vxeTableHandler">
    <template #group_name_edit="{ row }">
      <vxe-input v-model="row.group_name"></vxe-input>
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
import type { UnwrapRef } from 'vue';
import { message } from 'ant-design-vue';
import { VXETable, VxeGridInstance, VxeGridListeners, VxeGridProps } from 'vxe-table'
import type { SelectProps, FormProps } from 'ant-design-vue';

type SelectItem = {
  value: string;
  label: string;
};

interface FormState {
  group_name: string;
  character_name: string;
}

export default defineComponent({
  name: "EditGroups",
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
        { field: 'group_name', title: 'Group Name', editRender: {}, slots: { edit: 'group_name_edit' } },
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

            axios.post(`/api/topics/${props.topic}/groups`, {
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

    const createGroupName = ref<string>("")

    const handleCreateGroup = () => {
        axios.post(`/api/topics/${props.topic}/groups`, {
          "group_name": createGroupName.value,
          "character_name": ""
        })
        .then(response => {
          message.success(`Success to create group: ${createGroupName.value}`);
          initTableData();
        })
        .catch(error => {
          console.log(error);
        });
    }

    const formState: UnwrapRef<FormState> = reactive({
      group_name: '',
      character_name: '',
    });

    const handleSubmitForm: FormProps['onFinish'] = values => {
      axios.post(`/api/topics/${props.topic}/groups`, {
          "group_name": formState.group_name,
          "character_name": formState.character_name
        })
        .then(response => {
          message.success(`Success to add ${formState.character_name} to group ${formState.group_name}`);
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

    const selectGroupOptions = ref<SelectProps['options']>([]);

    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const initTableData = () => {
      axios.get(`/api/topics/${props.topic}/groups`)
        .then(response => {
          vxeTableOptions.data = response.data.groups;
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

        axios.get(`/api/topics/${props.topic}/groups_names`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.groups_names.forEach(group_name => {
            selectItems.push({"value": group_name, "label": group_name})
          });
          selectGroupOptions.value = [...selectItems];
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

      createGroupName,
      handleCreateGroup,

      formState,
      handleSubmitForm,
      handleSubmitFormFailed,

      filterOption,
      selectCharacterOptions,
      selectGroupOptions
    }
  }
})
</script>
