
<template>

  <div style="padding: 20px">
    <h1>{{$t('ManageTopics')}}</h1>

    <!-- Form to create topic -->
    <a-form layout="inline" :model="createTopicFormState" @finish="handleCreateTopicFinish" @finishFailed="handleFinishFailed">
      <a-form-item>
        <a-input v-model:value="createTopicFormState.name" :placeholder="$t('TopicName')">
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          {{$t('CreateTopic')}}
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to delete topic -->
    <a-form layout="inline" :model="deleteTopicFormState" @finish="handleDeleteTopicFinish"
      @finishFailed="handleFinishFailed">
      <a-form-item>
        <a-select v-model:value="deleteTopicFormState.name" show-search placeholder="Select topic" style="width: 200px"
          :options="selectTopicOptions" >
        </a-select>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          {{$t('DeleteTopic')}}
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to set topic official -->
    <a-form layout="inline" :model="setOfficialTopicFormState" @finish="handleSetOfficialTopicFinish"
      @finishFailed="handleFinishFailed">
      <a-form-item>
        <a-select v-model:value="setOfficialTopicFormState.name" show-search placeholder="Select topic" style="width: 200px"
          :options="selectTopicOptions" >
        </a-select>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          {{$t('SetOfficialTopic')}}
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to export topic -->
    <a-form layout="inline" :model="exportTopicFormState" @finish="handleExportTopic" >
      <a-form-item>
        <a-select v-model:value="exportTopicFormState.topic" show-search style="width: 200px"
          :options="selectTopicOptions" >
        </a-select>
      </a-form-item>
      <a-form-item>
        <a-input v-model:value="exportTopicFormState.path" :placeholder="$t('ExportDirectory')"></a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          {{$t('ExportTopic')}}
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to import topic -->
    <a-form layout="inline" :model="importTopicFormState" @finish="handleImportTopic" >
      <a-form-item>
        <a-input v-model:value="importTopicFormState.topic" :placeholder="$t('TopicName')"></a-input>
      </a-form-item>
      <a-form-item>
        <a-input v-model:value="importTopicFormState.path" :placeholder="$t('ImportDirectory')"></a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          {{$t('ImportTopic')}}
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to export all topics -->
    <a-form layout="inline" :model="exportAllTopicsFormState" @finish="handleExportAllTopics" >
      <a-form-item>
        <a-input v-model:value="exportAllTopicsFormState.path" :placeholder="$t('ExportDirectory')"></a-input>
      </a-form-item>
      <a-form-item>
        <a-switch v-model:checked="exportAllTopicsFormState.official" :checked-children="$t('Official')" :un-checked-children="$t('NotOfficial')" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          {{$t('ExportAllTopic')}}
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to import all topics -->
    <a-form layout="inline" :model="importAllTopicsFormState" @finish="handleImportAllTopics" >
      <a-form-item>
        <a-input v-model:value="importAllTopicsFormState.path" :placeholder="$t('ImportDirectory')"></a-input>
      </a-form-item>
      <a-form-item>
        <a-switch v-model:checked="importAllTopicsFormState.official" :checked-children="$t('Official')" :un-checked-children="$t('NotOfficial')" />
      </a-form-item>      
      <a-form-item>
        <a-button type="primary" html-type="submit">
          {{$t('importAllTopic')}}
        </a-button>
      </a-form-item>
    </a-form>

    <br /><br />
    <!-- List of all topics -->
    <all-topic-list></all-topic-list>

  </div>
</template>

<script lang="ts">
import type { FormProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';
import axios from 'axios';
import type { UnwrapRef } from 'vue';
import { defineComponent, onMounted, reactive, ref } from 'vue';
import AllTopicList from './AllTopicList.vue';

type SelectItem = {
  value: string;
  label: string;
};

interface CreateDeleteTopicFormState {
  name: string;
}

interface ImportExportTopicFormState {
  topic: string;
  path: string;
}

interface ImportExportTopicsFormState {
  path: string;
  official: boolean;
}

export default defineComponent({
  name: "EditTopics",
  props: {},
  components: {
    AllTopicList
  },
  setup() {
    const chosenTopicName = ref("");

    // Select options for selecting topic
    const selectTopicOptions = ref<SelectTypes['options']>([]);
    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const createTopicFormState: UnwrapRef<CreateDeleteTopicFormState> = reactive({
      name: ''
    });

    const deleteTopicFormState: UnwrapRef<CreateDeleteTopicFormState> = reactive({
      name: ''
    });

    const setOfficialTopicFormState: UnwrapRef<CreateDeleteTopicFormState> = reactive({
      name: ''
    });

    const exportTopicFormState: UnwrapRef<ImportExportTopicFormState> = reactive({
      topic: '',
      path: '',
    });

    const importTopicFormState: UnwrapRef<ImportExportTopicFormState> = reactive({
      topic: '',
      path: '',
    });

    const exportAllTopicsFormState: UnwrapRef<ImportExportTopicsFormState> = reactive({
      path: '',
      official: true
    });

    const importAllTopicsFormState: UnwrapRef<ImportExportTopicsFormState> = reactive({
      path: '',
      official: true
    });

    const handleCreateTopicFinish: FormProps['onFinish'] = values => {
      axios.post(`/api/topics`, {
        "name": createTopicFormState.name
      })
        .then(response => {
          message.success('Success to create topic: ' + createTopicFormState.name);
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleDeleteTopicFinish: FormProps['onFinish'] = values => {
      axios.delete(`/api/topics/${deleteTopicFormState.name}`)
        .then(response => {
          message.success('Success to delete topic: ' + deleteTopicFormState.name);
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleSetOfficialTopicFinish: FormProps['onFinish'] = values => {
      axios.put(`/api/topics/${setOfficialTopicFormState.name}/official`)
        .then(response => {
          message.success('Success to set offical topic: ' + setOfficialTopicFormState.name);
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleExportTopic: FormProps['onFinish'] = values => {
      axios.post(`/api/topics/${exportTopicFormState.topic}/export`, {
        path: exportTopicFormState.path
      })
      .then(response => {
        message.success('Success to export topic: ' + exportTopicFormState.topic);
        initTopicListData();
      })
      .catch(error => {
        console.log(error);
      });
    };

    const handleImportTopic: FormProps['onFinish'] = values => {
      axios.post(`/api/topics/${importTopicFormState.topic}/import`, {
        path: importTopicFormState.path
      })
      .then(response => {
        message.success('Success to import topic: ' + importTopicFormState.topic);
        initTopicListData();
      })
      .catch(error => {
        console.log(error);
      });
    };

    const handleExportAllTopics: FormProps['onFinish'] = values => {
      axios.post("/api/topics/export_all", {
        path: exportAllTopicsFormState.path,
        official: exportAllTopicsFormState.official
      })
      .then(response => {
        message.success("Success to export all topics");
        initTopicListData();
      })
      .catch(error => {
        console.log(error);
      });
    };

    const handleImportAllTopics: FormProps['onFinish'] = values => {
      axios.post("/api/topics/import_all", {
        path: importAllTopicsFormState.path,
        official: importAllTopicsFormState.official
      })
      .then(response => {
        message.success("Success to import all topics");
        initTopicListData();
      })
      .catch(error => {
        console.log(error);
      });
    };


    const handleFinishFailed: FormProps['onFinishFailed'] = errors => {
      console.log(errors);
    };

    const initTopicListData = () => {
      // TODO(tobe): Refresh child component of AllTopicList

      axios.get(`/api/topics`)
        .then(response => {
          // Set select options
          const selectItems: SelectItem[] = [];
          response.data.topics.forEach(theTopic => {
            selectItems.push({ "value": theTopic.name, "label": theTopic.name })
          });
          selectTopicOptions.value = [...selectItems];

        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      initTopicListData();
    })

    return {
      initTopicListData,

      chosenTopicName,
      createTopicFormState,
      handleCreateTopicFinish,
      deleteTopicFormState,
      handleDeleteTopicFinish,
      handleFinishFailed,
      setOfficialTopicFormState,
      handleSetOfficialTopicFinish,

      selectTopicOptions,
      filterOption,

      exportTopicFormState,
      importTopicFormState,
      handleExportTopic,
      handleImportTopic,

      exportAllTopicsFormState,
      importAllTopicsFormState,
      handleExportAllTopics,
      handleImportAllTopics
    }
  }
})
</script>
