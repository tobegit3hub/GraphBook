
<template>

<h1>Wizard to add new character</h1>

<div>

  <a-steps :current="currentStep">
    <a-step title="Create Character" />
    <a-step title="Add Relations" />
    <a-step title="Join Groups" />
  </a-steps>


  <div :style="{ background: '#fff', margin: '24px', padding: '24px' }">

    <!-- Form of creating a character-->
    <div v-show="currentStep === 0">
      <a-form
        :model="createCharacterFormState"
        @finish="submitCreateCharacterForm"
      >

      <a-form-item
          label="Name"
          name="name"
          :rules="[{ required: true, message: 'Please input name!' }]"
        >
          <a-input v-model:value="createCharacterFormState.name" />
        </a-form-item>

        <a-form-item
          label="Note"
          name="note"
        >
          <a-input v-model:value="createCharacterFormState.note" />
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
            :disabled="createCharacterFormState.name === ''"
          >
            Submit
          </a-button>
        </a-form-item>
      </a-form>

    </div>
  </div>


    <!-- Form of join groups-->
    <div v-show="currentStep === 1">
      
    <a-form ref="formRef" :model="dynamicValidateForm" v-bind="formItemLayoutWithOutLabel">
      <a-form-item
      v-for="(domain, index) in dynamicValidateForm.domains"
      :key="domain.key"
      v-bind="index === 0 ? formItemLayout : {}"
      :label="index === 0 ? 'Domains' : ''"
      :name="['domains', index, 'value']"
      :rules="{
        required: true,
        message: 'domain can not be null',
        trigger: 'change',
      }"
      >
      <a-input
        v-model:value="domain.value"
        placeholder="please input domain"
        style="width: 60%; margin-right: 8px"
      />
      <MinusCircleOutlined
        v-if="dynamicValidateForm.domains.length > 1"
        class="dynamic-delete-button"
        :disabled="dynamicValidateForm.domains.length === 1"
        @click="removeDomain(domain)"
      />
    </a-form-item>
    <a-form-item v-bind="formItemLayoutWithOutLabel">
      <a-button type="dashed" style="width: 60%" @click="addDomain">
        <PlusOutlined />
        Add group
      </a-button>
    </a-form-item>
    <a-form-item v-bind="formItemLayoutWithOutLabel">
      <a-button type="primary" html-type="submit" @click="submitForm">Submit</a-button>
    </a-form-item>
  </a-form>


  </div>




  <a-button v-if="currentStep < steps.length - 1" type="primary" @click="next">Next</a-button>
  <a-button
    v-if="currentStep == steps.length - 1"
    type="primary"
    @click="$message.success('Processing complete!')"
  >
    Done
  </a-button>
  <a-button v-if="currentStep > 0" style="margin-left: 8px" @click="prev">Previous</a-button>

</div>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'
import type { UnwrapRef } from 'vue';
import type { SelectProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';
import type { FormProps, UploadProps } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { ValidateErrorEntity } from 'ant-design-vue/es/form/interface';

type SelectItem = {
  value: string;
  label: string;
};

interface CreateCharacterFormState {
  name: string;
  note: string;
  image_name: string;
}

interface Domain {
  key: number;
  value: string;

}

export default defineComponent({
  name: "AddCharacterWizard",
  components: {
    UploadOutlined,
    MinusCircleOutlined,
    PlusOutlined,
  },
  props: {
    topic: String,
  },
  setup (props) {

    const currentStep = ref<number>(1);
    const next = () => {
      currentStep.value++;
    };
    const prev = () => {
      currentStep.value--;
    };


    const uploadImageFileList = ref<UploadProps['fileList']>([]);
    const createCharacterFormState: UnwrapRef<CreateCharacterFormState> = reactive({
      name: '',
      note: '',
      image_name: ''
    });

    const submitCreateCharacterForm: FormProps['onFinish'] = values => {
      let image_name = createCharacterFormState.image_name

      if (uploadImageFileList.value?.length != null) {
        if (uploadImageFileList.value.length > 0) {
          image_name = uploadImageFileList.value[uploadImageFileList.value.length-1].name
        }
      }

      axios.post(`http://127.0.0.1:7788/api/topics/${props.topic}/characters`, {
          "name": createCharacterFormState.name,
          "note": createCharacterFormState.note,
          "image_name": image_name
        })
        .then(response => {
          message.success(`Success to add character: ${createCharacterFormState.name}`);
        })
        .catch(error => {
          console.log(error);
        });
      };



      const formRef = ref();
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 4 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 20 },
      },
    };
    const formItemLayoutWithOutLabel = {
      wrapperCol: {
        xs: { span: 24, offset: 0 },
        sm: { span: 20, offset: 4 },
      },
    };
    const dynamicValidateForm: UnwrapRef<{ domains: Domain[] }> = reactive({
      domains: [],
    });
    const submitForm = () => {
      formRef.value
        .validate()
        .then(() => {
          console.log('values', dynamicValidateForm.domains);
        })
        .catch((error: ValidateErrorEntity<any>) => {
          console.log('error', error);
        });
    };

    const removeDomain = (item: Domain) => {
      let index = dynamicValidateForm.domains.indexOf(item);
      if (index !== -1) {
        dynamicValidateForm.domains.splice(index, 1);
      }
    };
    const addDomain = () => {
      dynamicValidateForm.domains.push({
        value: '',
        key: Date.now(),
      });
    };
    
    

    return {
      currentStep,
      steps: [
        {
          title: 'First',
          content: 'First-content',
        },
        {
          title: 'Second',
          content: 'Second-content',
        },
        {
          title: 'Last',
          content: 'Last-content',
        },
      ],
      next,
      prev,

      uploadImageFileList,
      createCharacterFormState,
      submitCreateCharacterForm,

      formRef,
      formItemLayout,
      formItemLayoutWithOutLabel,
      dynamicValidateForm,
      submitForm,
      removeDomain,
      addDomain,
    }
  }
})
</script>
