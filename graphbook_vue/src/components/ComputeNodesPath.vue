
<template>

  <h3>Compute Paths</h3>
  
  <a-select
    v-model:value="computePathSource"
    show-search
    placeholder="Select user"
    style="width: 200px"
    :options="computePathOptions"
    :filter-option="computePathFilterOption"
  ></a-select>

  <a-select
    v-model:value="computePathTarget"
    show-search
    placeholder="Select user"
    style="width: 200px"
    :options="computePathOptions"
    :filter-option="computePathFilterOption"
  ></a-select>

  <a-select
    v-model:value="isComputePathOnlyDirected"
    placeholder="Only directed"
    style="width: 200px"
    :options=computePathOnlyDirectedOptions
  ></a-select>

  <a-button type="primary"
    @click="handleClickComputePaths"
    >Compute paths
  </a-button>

  <a-list item-layout="horizontal" :data-source="computedPaths">
    <template #renderItem="{ item }">
      <a-list-item>{{ item }}</a-list-item>
    </template>
  </a-list>

</template>

<script>
import { defineComponent, ref, reactive, watch, toRefs, onMounted} from 'vue'

import axios from 'axios'

export default defineComponent({
  name: "ComputeNodesPath",
  props: {
    topic: String,
  },
  setup (props) {

    let allNodeNames = ref([]);
    const chooseUserCheckboxState = reactive({
      chooseUserIndeterminateState: false,
      isChooseAllUsers: false,
      currentChosenUserNames: [],
    });

    const onChooseAllUsers = e => {
      Object.assign(chooseUserCheckboxState, {
        currentChosenUserNames: e.target.checked ? allNodeNames.value : [],
        chooseUserIndeterminateState: false,
      });

      updateNodes();
    };

    watch(() => chooseUserCheckboxState.currentChosenUserNames, val => {
      chooseUserCheckboxState.chooseUserIndeterminateState = !!val.length && val.length < allNodeNames.value.length;
      chooseUserCheckboxState.isChooseAllUsers = val.length === allNodeNames.value.length;

      updateNodes();
    });

    onMounted(() => {

      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/characters`).then(response => {
        
        var nodeNameList = [];
        var computePathOptionList = [];

        response.data.characters.forEach(function(node) {
          nodeNameList.push(node["name"])
          computePathOptionList.push({value: node["name"], label: node["name"]})
        });

        allNodeNames.value =  nodeNameList;

        computePathOptions.value = computePathOptionList;


      }, response => {
          console.log("Fail to get nodes");
      }); 

    })


    const computePathOnlyDirectedOptions = ref([{value: "true", label: "true"}, {value: "false", label: "false"}])
    let computedPaths = ref([]);
    let isComputePathOnlyDirected = ref()
    const computePathOptions = ref([]);
    const computePathSource = ref("david");
    const computePathTarget = ref("lucy")

    const computePathFilterOption = (input, option) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const handleClickComputePaths = () => {

      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/paths`, {
        params: {
          source: computePathSource.value,
          target: computePathTarget.value,
          only_directed: isComputePathOnlyDirected.value === 'true'
          // TODO: Support cutoff
        }
      }).then(response => {
          computedPaths.value = response.data.paths;
      }, response => {
          console.log("Fail to get edges");
      });
    }

    return {
      allNodeNames,
      onChooseAllUsers,
      computedPaths,
      isComputePathOnlyDirected,
      computePathOptions,
      computePathOnlyDirectedOptions,
      computePathFilterOption,
      computePathSource,
      computePathTarget,
      handleClickComputePaths
    }

  }
})

</script>
