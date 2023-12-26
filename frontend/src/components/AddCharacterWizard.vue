
<template>

  <h1>{{$t('WizardToAddNewCharacter')}}</h1>

  <br/>
  <div>
    <a-steps :current="currentStep">
      <a-step :title="$t('CreateCharacter')" />
      <a-step :title="$t('AddRelations')" />
      <a-step :title="$t('JoinGroups')" />
    </a-steps>

    <div :style="{ background: '#fff', margin: '24px', padding: '24px' }">

      <!-- Form of creating a character-->
      <div v-show="currentStep === 0">
        <a-form :model="createCharacterFormState" @finish="submitCreateCharacterForm">

          <a-form-item :label="$t('Name')" name="name" :rules="[{ required: true, message: 'Please input name!' }]">
            <a-input v-model:value="createCharacterFormState.name" />
          </a-form-item>

          <a-form-item :label="$t('Alias')" name="alias">
            <a-input v-model:value="createCharacterFormState.alias" />
          </a-form-item>

          <a-form-item :label="$t('Note')" name="note">
            <a-textarea auto-size v-model:value="createCharacterFormState.note" />
          </a-form-item>

          <a-form-item>
            <a-button type="primary" html-type="submit" :disabled="createCharacterFormState.name === ''">
              {{$t('Submit')}}
            </a-button>
          </a-form-item>
        </a-form>

      </div>
    </div>

    <!-- Form of add relations -->
    <div v-show="currentStep === 1">

      <a-form :model="addUpstreamRelationsForm">
        <div v-for="(addRelationItem, index) in addUpstreamRelationsForm.addRelationItems" :key="addRelationItem.key">

          <a-form layout="inline">
            <a-form-item>
              <span>{{$t('UpstreamCharacter')}}: </span>
              <a-select v-model:value="addRelationItem.character_name" show-search placeholder="Select character"
                style="width: 200px" :options="selectCharacterOptions" :filter-option="filterOption"></a-select>
            </a-form-item>

            <a-form-item :label="$t('Relation')" name="relation">
              <!-- TODO: not work of :rules="[{ required: true, message: 'Please input relation!' }]" -->
              <a-input v-model:value="addRelationItem.relation" />
            </a-form-item>

            <a-form-item :label="$t('Note')" name="note">
              <a-input v-model:value="addRelationItem.note" />
            </a-form-item>

            <MinusCircleOutlined v-if="addUpstreamRelationsForm.addRelationItems.length > 1"
              class="dynamic-delete-button" :disabled="addUpstreamRelationsForm.addRelationItems.length === 1"
              @click="removeUpstreamRelationItem(addRelationItem)" />
          </a-form>
        </div>

        <br />
        <a-form-item>
          <a-button type="dashed" style="width: 60%" @click="addUpstreamRelationItem">
            <PlusOutlined />
            {{$t('AddUpstreamRelation')}}
          </a-button>
        </a-form-item>
      </a-form>

      <br /><br />

      <a-form :model="addDownstreamRelationsForm">
        <div v-for="(addRelationItem, index) in addDownstreamRelationsForm.addRelationItems" :key="addRelationItem.key">

          <a-form layout="inline">
            <a-form-item>
              <span>{{$t('DownstreamCharacter')}}: </span>
              <a-select v-model:value="addRelationItem.character_name" show-search placeholder="Select character"
                style="width: 200px" :options="selectCharacterOptions" :filter-option="filterOption"></a-select>
            </a-form-item>

            <a-form-item :label="$t('Relation')" name="relation">
              <!-- TODO: not work of :rules="[{ required: true, message: 'Please input relation!' }]" -->
              <a-input v-model:value="addRelationItem.relation" />
            </a-form-item>

            <a-form-item :label="$t('Note')" name="note">
              <a-input v-model:value="addRelationItem.note" />
            </a-form-item>

            <MinusCircleOutlined v-if="addDownstreamRelationsForm.addRelationItems.length > 1"
              class="dynamic-delete-button" :disabled="addDownstreamRelationsForm.addRelationItems.length === 1"
              @click="removeDownstreamRelationItem(addRelationItem)" />
          </a-form>
        </div>

        <br />
        <a-form-item>
          <a-button type="dashed" style="width: 60%" @click="addDownstreamRelationItem">
            <PlusOutlined />
            {{$t('AddDownstreamRelation')}}
          </a-button>
        </a-form-item>
      </a-form>

      <a-form>
        <a-form-item>
          <a-button type="primary" html-type="submit" @click="submitAddRelationsForm">
            {{$t('Submit')}}
          </a-button>
        </a-form-item>
      </a-form>
    </div>


    <!-- Form of join groups-->
    <div v-show="currentStep === 2">

      <a-form :model="joinGroupsForm">
        <a-form-item v-for="(joinGroupItem, index) in joinGroupsForm.joinGroupItems" :key="joinGroupItem.key">

          <span>{{$t('Group')}}: </span>
          <a-select v-model:value="joinGroupItem.group_name" show-search placeholder="Select group" style="width: 200px"
            :options="selectGroupOptions" :filter-option="filterOption"></a-select>

          <MinusCircleOutlined v-if="joinGroupsForm.joinGroupItems.length > 1" class="dynamic-delete-button"
            :disabled="joinGroupsForm.joinGroupItems.length === 1" @click="removeJoinGroupItem(joinGroupItem)" />
        </a-form-item>
        <a-form-item>
          <a-button type="dashed" style="width: 60%" @click="addJoinGroupItem">
            <PlusOutlined />
            
          </a-button>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit" @click="submitJoinGroupsForm">
            {{$t('Submit')}}
          </a-button>
        </a-form-item>
      </a-form>
    </div>

    <a-button v-if="currentStep > 0" style="margin-left: 8px" @click="prevStep">{{$t('PreviousStep')}}</a-button>
    <a-button v-if="currentStep < totalStepCount - 1" type="primary" @click="nextStep">{{$t('NextStep')}}</a-button>
    <a-button v-if="currentStep == totalStepCount - 1" type="primary" @click="refreshCurrentPage">
      {{$t('Done')}}
    </a-button>

  </div>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted, watch } from 'vue'
import type { UnwrapRef } from 'vue';
import type { SelectProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';
import type { FormProps, UploadProps } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { useRouter, useRoute } from 'vue-router'

interface SelectItem {
  value: string;
  label: string;
};

interface CreateCharacterFormState {
  name: string;
  alias: string;
  note: string;
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
    const API_BASE_URI = axios.defaults.baseURL;

    const router = useRouter()
    const route = useRoute()

    const currentStep = ref<number>(0);
    const totalStepCount = 3;
    const nextStep = () => {
      currentStep.value++;
    };
    const prevStep = () => {
      currentStep.value--;
    };

    /* Create character */
    const createCharacterFormState: UnwrapRef<CreateCharacterFormState> = reactive({
      name: '',
      alias: '',
      note: '',
    });

    const submitCreateCharacterForm: FormProps['onFinish'] = values => {
      axios.post(`/api/topics/${props.topic}/characters`, {
        "name": createCharacterFormState.name,
        "alias": createCharacterFormState.alias,
        "note": createCharacterFormState.note,
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
        axios.post(`/api/topics/${props.topic}/relations`, {
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
        axios.post(`/api/topics/${props.topic}/groups`, {
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

    const refreshCurrentPage = () => {
      window.location.reload()
    }

    watch(() => props.topic, (first, second) => {
      init();
    });

    const init = () => {
      axios.get(`/api/topics/${props.topic}/characters`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.characters.forEach(character => {
            selectItems.push({ "value": character.name, "label": character.name })
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
            selectItems.push({ "value": group_name, "label": group_name })
          });
          selectGroupOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      init();
    })

    return {
      API_BASE_URI,

      currentStep,
      totalStepCount,
      nextStep,
      prevStep,

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
      selectGroupOptions,

      refreshCurrentPage
    }
  }
})
</script>
