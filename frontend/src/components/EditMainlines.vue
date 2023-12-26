
<template>

  <h1>{{ $t('AddMainlineEvent') }}</h1>
  <a-form :model="formState" @finish="handleSubmitForm" @finishFailed="handleSubmitFormFailed">

    <a-form-item :label="$t('BranchName')" :rules="[{ required: true, message: 'Please input branch name!' }]">
      <a-select v-model:value="formState.branch" show-search style="width: 200px" :options="selectBranchOptions"
        :filter-option="filterOption"></a-select>
      <a-input v-model:value="formState.branch" />
    </a-form-item>

    <a-form-item :label="$t('EventName')" :rules="[{ required: true, message: 'Please input event name!' }]">
      <a-input v-model:value="formState.event" />
    </a-form-item>

    <a-form-item :label="$t('Note')">
      <a-textarea auto-size v-model:value="formState.note" />
    </a-form-item>

    <a-form-item>
      <span>{{ $t('PreviousEvent') }}: &nbsp;</span>
      <a-select v-model:value="formState.previous_event" show-search style="width: 200px" :options="selectEventOptions"
        :filter-option="filterOption"></a-select>
    </a-form-item>

    <a-form-item>
      <span>{{ $t('FinalEvent') }}: &nbsp;</span>
      <a-select v-model:value="formState.final_event" show-search style="width: 200px" :options="selectEventOptions"
        :filter-option="filterOption"></a-select>
    </a-form-item>

    <a-form-item>
      <a-button type="primary" html-type="submit"
        :disabled="formState.group_name === '' || formState.character_name === ''">
        {{ $t('Submit') }}
      </a-button>
    </a-form-item>
  </a-form>

  <br />
  <h1>{{ $t('MainlinesTable') }}</h1>
  <vxe-grid ref="vxeTable" v-bind="vxeTableOptions" v-on="vxeTableHandler">
    <template #branch_edit="{ row }">
      <vxe-input v-model="row.branch"></vxe-input>
    </template>
    <template #event_edit="{ row }">
      <vxe-input v-model="row.event"></vxe-input>
    </template>
    <template #note_edit="{ row }">
      <vxe-input v-model="row.note"></vxe-input>
    </template>
    <template #previous_event_edit="{ row }">
      <vxe-input v-model="row.previous_event"></vxe-input>
    </template>
    <template #final_event_edit="{ row }">
      <vxe-input v-model="row.final_event"></vxe-input>
    </template>

    <template #operate="{ row }" slot-scope="scope">
      <vxe-button @click="removeRow(row)" circle status="warning" icon="fa fa-trash-o"></vxe-button>
    </template>
  </vxe-grid>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted } from 'vue'
import type { UnwrapRef } from 'vue';
import { message } from 'ant-design-vue';
import { VXETable, VxeGridInstance, VxeGridListeners, VxeGridProps } from 'vxe-table'
import type { SelectProps, FormProps } from 'ant-design-vue';

type SelectItem = {
  value: string;
  label: string;
};

interface FormState {
  branch: string;
  event: string;
  note: string;
  previous_event: string;
  final_event: string;
}

export default defineComponent({
  name: "EditMainlines",
  props: {
    topic: String,
  },
  setup(props) {
    const vxeTable = ref<VxeGridInstance>()
    const vxeTableOptions = reactive<VxeGridProps>({
      border: true,
      keepSource: true,
      id: 'mainlines_table',
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
        { field: 'branch', title: 'Branch', editRender: {}, slots: { edit: 'branch_edit' } },
        { field: 'event', title: 'Event', editRender: {}, slots: { edit: 'event_edit' } },
        { field: 'note', title: 'Note', editRender: {}, slots: { edit: 'note_edit' } },
        { field: 'previous_event', title: 'Previous Event', editRender: {}, slots: { edit: 'previous_event_edit' } },
        { field: 'final_event', title: 'Final Event', editRender: {}, slots: { edit: 'final_event_edit' } },
        { title: 'Delete', width: 200, slots: { default: 'operate' } }
      ],
      toolbarConfig: {
        buttons: [
          { code: 'insertButton', name: 'New', status: 'primary' },
          { code: 'saveButton', name: 'Save', status: 'success' }
        ],
        import: false,
        export: true,
        zoom: true,
        custom: true,
        refresh: false
      },
      data: []
    })

    const vxeTableHandler: VxeGridListeners = {
      toolbarButtonClick({ code }) {
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

            axios.post(`/api/topics/${props.topic}/mainlines`, {
              insert_mainlines: insertRecords,
              update_mainlines: updateRecords,
              delete_mainlines: removeRecords
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
      branch: '',
      event: '',
      note: '',
      previous_event: '',
      final_event: ''
    });

    const handleSubmitForm: FormProps['onFinish'] = values => {
      axios.post(`/api/topics/${props.topic}/mainlines`, {
        branch: formState.branch,
        event: formState.event,
        note: formState.note,
        previous_event: formState.previous_event,
        final_event: formState.final_event
      })
        .then(response => {
          message.success(`Success to add ${formState.event} to branch ${formState.branch}`);
          init();
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleSubmitFormFailed: FormProps['onFinishFailed'] = errors => {
      console.log("Fail to submit form: " + errors);
    };

    const selectBranchOptions = ref<SelectProps['options']>([]);
    const selectEventOptions = ref<SelectProps['options']>([]);

    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const init = () => {
      axios.get(`/api/topics/${props.topic}/mainlines`)
        .then(response => {
          vxeTableOptions.data = response.data.mainlines;
        })
        .catch(error => {
          console.log(error);
        });

      axios.get(`/api/topics/${props.topic}/mainlines/events`)
        .then(response => {
          const selectItems: SelectItem[] = [{ "value": "", "label": "" }];
          response.data.events.forEach(item => {
            selectItems.push({ "value": item.event, "label": item.branch + " - " + item.event })
          });
          selectEventOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
        });

      axios.get(`/api/topics/${props.topic}/mainlines/branches`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.branches.forEach(branch => {
            selectItems.push({ "value": branch, "label": branch })
          });
          selectBranchOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      init();
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
      selectEventOptions,
      selectBranchOptions

    }
  }
})
</script>
