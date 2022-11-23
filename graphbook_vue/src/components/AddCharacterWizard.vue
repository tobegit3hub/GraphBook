
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
        <a-form :model="createCharacterFormState" @finish="submitCreateCharacterForm">

          <a-form-item label="Name" name="name" :rules="[{ required: true, message: 'Please input name!' }]">
            <a-input v-model:value="createCharacterFormState.name" />
          </a-form-item>

          <a-form-item label="Note" name="note">
            <a-input v-model:value="createCharacterFormState.note" />
          </a-form-item>

          <a-form-item>
            <a-upload v-model:fileList="uploadImageFileList"
              :action="`http://127.0.0.1:7788/api/topics/${topic}/character_image`" list-type="picture"
              :multiple="false">
              <a-button>
                <upload-outlined></upload-outlined>
                Upload image
              </a-button>
            </a-upload>

          </a-form-item>

          <a-form-item>
            <a-button type="primary" html-type="submit" :disabled="createCharacterFormState.name === ''">
              Submit
            </a-button>
          </a-form-item>
        </a-form>

      </div>
    </div>

    <!-- Form of add relations -->
    <div v-show="currentStep === 1">

      <a-form :model="addUpstreamRelationsForm" >
        <div v-for="(addRelationItem, index) in addUpstreamRelationsForm.addRelationItems" :key="addRelationItem.key">

          <a-form layout="inline">
            <a-form-item>
              <span>Upstream character: </span>
              <a-select
                v-model:value="addRelationItem.character_name"
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
            >
            <!-- TODO: not work of :rules="[{ required: true, message: 'Please input relation!' }]" -->
              <a-input v-model:value="addRelationItem.relation" />
            </a-form-item>

            <a-form-item
              label="note"
              name="note"
            >
              <a-input v-model:value="addRelationItem.note" />
            </a-form-item>
                    
            <MinusCircleOutlined v-if="addUpstreamRelationsForm.addRelationItems.length > 1" class="dynamic-delete-button"
              :disabled="addUpstreamRelationsForm.addRelationItems.length === 1" @click="removeUpstreamRelationItem(addRelationItem)" />
          </a-form>
        </div>

        <br />
        <a-form-item>
          <a-button type="dashed" style="width: 60%" @click="addUpstreamRelationItem">
            <PlusOutlined />
            Add upstream relation
          </a-button>
        </a-form-item>
      </a-form>

      <br /><br />

      <a-form :model="addDownstreamRelationsForm" >
        <div v-for="(addRelationItem, index) in addDownstreamRelationsForm.addRelationItems" :key="addRelationItem.key">

          <a-form layout="inline">
            <a-form-item>
              <span>Downstream character: </span>
              <a-select
                v-model:value="addRelationItem.character_name"
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
            >
            <!-- TODO: not work of :rules="[{ required: true, message: 'Please input relation!' }]" -->            
              <a-input v-model:value="addRelationItem.relation" />
            </a-form-item>

            <a-form-item
              label="note"
              name="note"
            >
              <a-input v-model:value="addRelationItem.note" />
            </a-form-item>
                    
            <MinusCircleOutlined v-if="addDownstreamRelationsForm.addRelationItems.length > 1" class="dynamic-delete-button"
              :disabled="addDownstreamRelationsForm.addRelationItems.length === 1" @click="removeDownstreamRelationItem(addRelationItem)" />
          </a-form>
        </div>

        <br />
        <a-form-item>
          <a-button type="dashed" style="width: 60%" @click="addDownstreamRelationItem">
            <PlusOutlined />
            Add downstream relation
          </a-button>
        </a-form-item>
      </a-form>

       <a-form>
        <a-form-item>
            <a-button type="primary" html-type="submit" @click="submitAddRelationsForm">Submit</a-button>
          </a-form-item>
       </a-form>
    </div>


    <!-- Form of join groups-->
    <div v-show="currentStep === 2">

      <a-form :model="joinGroupsForm">
        <a-form-item v-for="(joinGroupItem, index) in joinGroupsForm.joinGroupItems" :key="joinGroupItem.key"
          label="Group:">

          <a-select v-model:value="joinGroupItem.group_name" show-search placeholder="Select group" style="width: 200px"
            :options="selectGroupOptions" :filter-option="filterOption"></a-select>

          <MinusCircleOutlined v-if="joinGroupsForm.joinGroupItems.length > 1" class="dynamic-delete-button"
            :disabled="joinGroupsForm.joinGroupItems.length === 1" @click="removeJoinGroupItem(joinGroupItem)" />
        </a-form-item>
        <a-form-item>
          <a-button type="dashed" style="width: 60%" @click="addJoinGroupItem">
            <PlusOutlined />
            Join group
          </a-button>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit" @click="submitJoinGroupsForm">Submit</a-button>
        </a-form-item>
      </a-form>
    </div>

    <a-button v-if="currentStep > 0" style="margin-left: 8px" @click="prevStep">Previous</a-button>
    <a-button v-if="currentStep < totalStepCount - 1" type="primary" @click="nextStep">Next</a-button>
    <a-button v-if="currentStep == totalStepCount - 1" type="primary" @click="">
      Done
    </a-button>


  </div>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted } from 'vue'
import type { UnwrapRef } from 'vue';
import type { SelectProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';
import type { FormProps, UploadProps } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue';

interface SelectItem {
  value: string;
  label: string;
};

interface CreateCharacterFormState {
  name: string;
  note: string;
  image_name: string;
}

interface AddRelationItem {
  key: number;
  character_name: string;
  relation: string;
  note: string;
}

interface JoinGroupItem {
  key: number;
  group_name: string;
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
  setup(props) {

    const currentStep = ref<number>(0);
    const totalStepCount = 3;
    const nextStep = () => {
      currentStep.value++;
    };
    const prevStep = () => {
      currentStep.value--;
    };

    /* Create character */
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
          image_name = uploadImageFileList.value[uploadImageFileList.value.length - 1].name
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

    /* Add relations */
    const addUpstreamRelationsForm: UnwrapRef<{ addRelationItems: AddRelationItem[] }> = reactive({
      addRelationItems: [],
    });

    const addUpstreamRelationItem = () => {
      addUpstreamRelationsForm.addRelationItems.push({
        key: Date.now(),
        character_name: '',
        relation: '',
        note: ''
      });
    };

    const removeUpstreamRelationItem = (item: AddRelationItem) => {
      let index = addUpstreamRelationsForm.addRelationItems.indexOf(item);
      if (index !== -1) {
        addUpstreamRelationsForm.addRelationItems.splice(index, 1);
      }
    };

    const addDownstreamRelationsForm: UnwrapRef<{ addRelationItems: AddRelationItem[] }> = reactive({
      addRelationItems: [],
    });

    const addDownstreamRelationItem = () => {
      addDownstreamRelationsForm.addRelationItems.push({
        key: Date.now(),
        character_name: '',
        relation: '',
        note: ''
      });
    };

    const removeDownstreamRelationItem = (item: AddRelationItem) => {
      let index = addDownstreamRelationsForm.addRelationItems.indexOf(item);
      if (index !== -1) {
        addDownstreamRelationsForm.addRelationItems.splice(index, 1);
      }
    };

    const submitAddRelationsForm = () => {
      if (createCharacterFormState.name) {
        axios.post(`http://127.0.0.1:7788/api/topics/${props.topic}/relations`, {
          "character_name": createCharacterFormState.name,
          "upstream_relations": addUpstreamRelationsForm.addRelationItems,
          "downstream_relations": addDownstreamRelationsForm.addRelationItems
        })
        .then(response => {
          message.success(`Success to add relations for ${createCharacterFormState.name}`);
        })
        .catch(error => {
          console.log(error);
        });
      } else {
        message.warn("The character name is empty, please set in previous step")
      }
    };

    const selectCharacterOptions = ref<SelectProps['options']>([]);

    /* Join grouops */
    const joinGroupsForm: UnwrapRef<{ joinGroupItems: JoinGroupItem[] }> = reactive({
      joinGroupItems: [],
    });

    const addJoinGroupItem = () => {
      joinGroupsForm.joinGroupItems.push({
        key: Date.now(),
        group_name: '',
      });
    };

    const removeJoinGroupItem = (item: JoinGroupItem) => {
      let index = joinGroupsForm.joinGroupItems.indexOf(item);
      if (index !== -1) {
        joinGroupsForm.joinGroupItems.splice(index, 1);
      }
    };

    const submitJoinGroupsForm = () => {
      let groupsNames: string[] = [];
      joinGroupsForm.joinGroupItems.forEach((joinGroupItem) => {
        groupsNames.push(joinGroupItem.group_name);
      });

      if (createCharacterFormState.name) {
        axios.post(`http://127.0.0.1:7788/api/topics/${props.topic}/groups`, {
          "groups_names": groupsNames,
          "character_name": createCharacterFormState.name
        })
          .then(response => {
            message.success(`Success to join the groups: ${groupsNames}`);
          })
          .catch(error => {
            console.log(error);
          });
      } else {
        message.warn("The character name is empty, please set in previous step")
      }
    };

    const selectGroupOptions = ref<SelectProps['options']>([]);

    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };


    onMounted(() => {
      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/characters`)
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
      
      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/groups_names`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.groups.forEach(group => {
            selectItems.push({ "value": group.name, "label": group.name })
          });
          selectGroupOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
        });
    })


    return {
      currentStep,
      totalStepCount,
      nextStep,
      prevStep,

      uploadImageFileList,
      createCharacterFormState,
      submitCreateCharacterForm,

      addUpstreamRelationsForm,
      addUpstreamRelationItem,
      removeUpstreamRelationItem,
      addDownstreamRelationsForm,
      addDownstreamRelationItem,
      removeDownstreamRelationItem,
      submitAddRelationsForm,
      selectCharacterOptions,
      filterOption,

      joinGroupsForm,
      addJoinGroupItem,
      removeJoinGroupItem,
      submitJoinGroupsForm,
      selectGroupOptions
    }
  }
})
</script>
