
<template>
  <div style="padding: 20px">
    <h1>Compute Paths</h1>

    <a-form layout="inline">

      <a-form-item>
        <a-select v-model:value="computePathSource" show-search placeholder="Select user" style="width: 200px"
          :options="computePathOptions" :filter-option="computePathFilterOption"></a-select>
      </a-form-item>

      <a-form-item>
        <a-select v-model:value="computePathTarget" show-search placeholder="Select user" style="width: 200px"
          :options="computePathOptions" :filter-option="computePathFilterOption"></a-select>
      </a-form-item>

      <a-form-item>
        <a-select v-model:value="isComputePathOnlyDirected" placeholder="Only directed" style="width: 200px"
          :options=computePathOnlyDirectedOptions></a-select>

      </a-form-item>

      <a-form-item>
        <a-input v-model:value="computePathCutoff" placeholder="Cutoff of paths" />
      </a-form-item>

      <a-form-item>
        <a-button type="primary" @click="handleClickComputePaths">Compute paths
        </a-button>
      </a-form-item>
    </a-form>

    <br /><br />
    <a-list item-layout="horizontal" size="large" bordered :data-source="computedPaths">
      <template #renderItem="{ item }">
        <a-list-item @click="selectPathItem(item)">{{ item.join(" -> ") }}</a-list-item>
      </template>
    </a-list>

  </div>

</template>

<script>
import { defineComponent, ref, reactive, watch, onMounted } from 'vue'

import axios from 'axios'

export default defineComponent({
  name: "ComputePaths",
  props: {
    topic: String,
  },
  setup(props) {

    let allCharactersNames = ref([]);
    const chooseUserCheckboxState = reactive({
      chooseUserIndeterminateState: false,
      isChooseAllUsers: false,
      currentChosenUserNames: [],
    });

    const onChooseAllUsers = e => {
      Object.assign(chooseUserCheckboxState, {
        currentChosenUserNames: e.target.checked ? allCharactersNames.value : [],
        chooseUserIndeterminateState: false,
      });

      updateNodes();
    };

    watch(() => chooseUserCheckboxState.currentChosenUserNames, val => {
      chooseUserCheckboxState.chooseUserIndeterminateState = !!val.length && val.length < allCharactersNames.value.length;
      chooseUserCheckboxState.isChooseAllUsers = val.length === allCharactersNames.value.length;

      updateNodes();
    });

    watch(() => props.topic, (first, second) => {
      init();
    });

    const init = () => {
      axios.get(`/api/topics/${props.topic}/characters`).then(response => {

        var charactersNameList = [];
        var computePathOptionList = [];

        response.data.characters.forEach(function (character) {
          charactersNameList.push(character["name"])
          computePathOptionList.push({ value: character["name"], label: character["name"] })
        });

        allCharactersNames.value = charactersNameList;

        computePathOptions.value = computePathOptionList;
      }, response => {
        console.log("Fail to get nodes");
      });
    }

    onMounted(() => {
      init();
    })

    const computePathOnlyDirectedOptions = ref([{ value: "true", label: "true" }, { value: "false", label: "false" }])
    let computedPaths = ref([]);
    let isComputePathOnlyDirected = ref()
    const computePathOptions = ref([]);
    const computePathSource = ref();
    const computePathTarget = ref();
    // tobedev
    //const computePathSource = ref("Dorio");
    //const computePathTarget = ref("Faraday");
    const computePathCutoff = ref();

    const computePathFilterOption = (input, option) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const handleClickComputePaths = () => {
      let intCutoff = -1;
      if (computePathCutoff.value) {
        intCutoff = parseInt(computePathCutoff.value)
      }
      axios.get(`/api/topics/${props.topic}/paths`, {
        params: {
          source: computePathSource.value,
          target: computePathTarget.value,
          only_directed: isComputePathOnlyDirected.value === 'true',
          cutoff: intCutoff
        }
      }).then(response => {
        computedPaths.value.splice(0);
        response.data.paths.forEach((path_data) => {
          // computedPaths.value.push(path_data.join("->"));
          computedPaths.value.push(path_data);
        })
      }, response => {
        console.log("Fail to get edges");
      });
    }


    /**
     * Select the item of result paths and get nodes/edges to update the graph.
     */
    const selectPathItem = (path_item) => {
      console.log(path_item);

      axios.get(`/api/topics/${props.topic}/path_data`, { params: {
        "characters_names": path_item
      }})
      .then(response => {
        // tobedev
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
      });

    }

    return {
      allCharactersNames,
      onChooseAllUsers,
      computedPaths,
      isComputePathOnlyDirected,
      computePathOptions,
      computePathOnlyDirectedOptions,
      computePathFilterOption,
      computePathSource,
      computePathTarget,
      computePathCutoff,
      handleClickComputePaths,

      selectPathItem
    }

  }
})

</script>
