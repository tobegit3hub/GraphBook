
<template>

<a-form
    layout="inline"
    :model="formState"
    @finish="handleSubmitForm"
    @finishFailed="handleSubmitFormFailed"
  >


  <a-form-item
      label="Name"
      name="name"
      :rules="[{ required: true, message: 'Please input name!' }]"
    >
      <a-input v-model:value="formState.name" />
    </a-form-item>

    <a-form-item
      label="Note"
      name="note"
    >
      <a-input v-model:value="formState.note" />
    </a-form-item>

    <a-form-item>
      <a-upload
      v-model:fileList="uploadImageFileList"
      :action="`http://127.0.0.1:7788/api/topics/${topic}/character_image`"
      list-type="picture"
      :multiple="false"
      >
        <a-button>
          <upload-outlined></upload-outlined>
          Upload image
        </a-button>
      </a-upload>

    </a-form-item>


    <a-form-item>
      <a-button
        type="primary"
        html-type="submit"
        :disabled="formState.name === ''"
      >
        Add
      </a-button>
    </a-form-item>
  </a-form>

  <vxe-grid ref="vxeTable" v-bind="vxeTableOptions" v-on="vxeTableHandler">
    <template #name_edit="{ row }">
      <vxe-input v-model="row.name"></vxe-input>
    </template>
    <template #note_edit="{ row }">
      <vxe-textarea v-model="row.note" :autosize="{ minRows: 1, maxRows: 8 }"></vxe-textarea>
    </template>
    <template #weight_edit="{ row }">
      <vxe-input v-model="row.weight"></vxe-input>
    </template>
    <template #image_name_edit="{ row }">
      <vxe-input v-model="row.image_name"></vxe-input>
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
import type { FormProps, UploadProps } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';

interface FormState {
  name: string;
  note: string;
  image_name: string;
}

export default defineComponent({
  name: "EditCharacters",
  components: {
    UploadOutlined
  },
  props: {
    topic: String,
  },
  setup (props) {
    const vxeTable = ref<VxeGridInstance>()
    const vxeTableOptions = reactive<VxeGridProps>({
      border: true,
      keepSource: true,
      id: 'characters_table',
      exportConfig: {},
      importConfig: {},
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
        { field: 'name', title: 'Name', editRender: {}, slots: { edit: 'name_edit' } },
        { field: 'note', title: 'Note', editRender: {}, slots: { edit: 'note_edit' } },
        { field: 'weight', title: 'Weight', slots: { edit: 'weight_edit' } },
        { field: 'image_name', title: 'Image name', editRender: {}, slots: { edit: 'image_name_edit' } },
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

            axios.post(`http://127.0.0.1:7788/api/topics/${props.topic}/characters`, {
              insert_characters: insertRecords,
              update_characters: updateRecords,
              delete_characters: removeRecords
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


    const uploadImageFileList = ref<UploadProps['fileList']>([]);

    const formState: UnwrapRef<FormState> = reactive({
      name: '',
      note: '',
      image_name: ''
    });
    
    const handleSubmitForm: FormProps['onFinish'] = values => {

      let image_name = formState.image_name

      if (uploadImageFileList.value?.length != null) {
        if (uploadImageFileList.value.length > 0) {
          image_name = uploadImageFileList.value[uploadImageFileList.value.length-1].name
        }
      }

      axios.post(`http://127.0.0.1:7788/api/topics/${props.topic}/characters`, {
          "name": formState.name,
          "note": formState.note,
          "image_name": image_name
        })
        .then(response => {
          message.success(`Success to add character: ${formState.name}`);
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleSubmitFormFailed: FormProps['onFinishFailed'] = errors => {
      console.log("Fail to submit form: " + errors);
    };

    onMounted(() => {
      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/characters`)
        .then(response => {
          vxeTableOptions.data = response.data.characters;
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

      uploadImageFileList,
      formState,
      handleSubmitForm,
      handleSubmitFormFailed,
    }
  }
})
</script>
