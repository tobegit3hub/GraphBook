
<template>

  <br />
  <!-- Echarts Graph -->
  <v-chart class="chart" :option="vuechartOption" @click="handleClickGraph" />

  <div v-show="!onlyGraph">
    <!-- The modal to show character -->
    <a-modal v-model:visible="isCharacterModalVisible" :title="currentCharacterModalName" @ok="handleCharacterModalOk">
      <p>{{ $t('message.Name') }}: <router-link :to='`/topics/${topic}/characters/${currentCharacterModalName}`'>{{
          currentCharacterModalName
      }}</router-link>
      </p>
      <p>{{ $t('message.Weight') }}: {{ currentCharacterModalWeight }}</p>
      <a-image v-if="currentCharacterModalImageName"
        :src="`${API_BASE_URI}/images/${topic}/${currentCharacterModalImageName}`" />
      <br /><br />
      <p>{{ $t('message.Note') }}:</p>
      <p>{{ currentModalNote }}</p>
    </a-modal>

    <!-- Edit Graph -->
    <br />
    <h2>{{ $t('message.Edit') }}</h2>
    <a-button type="primary" @click="showEditGraphDrawer">{{ $t('message.GraphParameters') }}</a-button>

    <br /><br />
    <h2>{{ $t('message.Characters') }}</h2>
    <div>
      <a-checkbox v-model:checked="isChooseAllCharacters" :indeterminate="isChooseCharacterIndeterminateState"
        @change="handleChooseAllCharacters">
        {{ $t('message.ChooseAll') }}
      </a-checkbox>
    </div>
    <a-checkbox-group v-model:value="currentChosenCharacterNames" :options="allCharacterNames" />

    <br /><br />
    <h2>{{ $t('message.Groups') }}</h2>
    <div>
      <a-checkbox v-model:checked="isChooseAllGroups" :indeterminate="isChooseGroupIndeterminateState"
        @change="handleChooseAllGroups">
        {{ $t('message.ChooseAll') }}
      </a-checkbox>
    </div>
    <a-checkbox-group v-model:value="currentChosenGroupNames" :options="allGroupNames" />

    <br /><br />
    <h2>{{ $t('message.GraphAnimation') }}</h2>
    <div>
      <a-row>
        <a-col :span="8">
          <a-slider v-model:value="playGraphInterval" :min="10" :max="10000" />
        </a-col>
        <a-col :span="8">
          <a-button type="primary" @click="handlePlayGraph">{{ $t('message.Play') }}</a-button>
          <a-button type="danger" @click="handleStopPlayGraph">{{ $t('message.Stop') }}</a-button>
        </a-col>
      </a-row>
    </div>

    <!-- The drawer to edit graph -->
    <a-drawer v-model:visible="isEditGraphDrawerVisible" :title="$t('message.GraphParameters')" placement="right">

      <p>{{ $t('message.ShowTitle') }}</p>
      <a-switch v-model:checked="isShowTitle" @change="init" />

      <br /><br />
      <p>{{ $t('message.ImageMode') }}</p>
      <a-switch v-model:checked="isDisplayImage" @change="init" />

      <br /><br />
      <p>{{ $t('message.RoamScaleMode') }}</p>
      <a-switch v-model:checked="isEnableScale" @change="changeIsEnableScale" />

      <br /><br />
      <p>{{ $t('message.CharactrWeightMode') }}</p>
      <a-switch v-model:checked="isEnableCharacterWeight" @change="handleEnableCharacterWeight" />

      <br /><br />
      <p>{{ $t('message.CharactrSize') }}</p>
      <a-slider :max="200" v-model:value="symbolSize" @change="handleEnableCharacterWeight" />

      <br /><br />
      <p>{{ $t('message.CharacterFontSize') }}</p>
      <a-slider :min="0" :max="40" v-model:value="labelFontSize" @change="changeSymbolFontSize" />

      <br /><br />
      <p>{{ $t('message.RelationFontSize') }}</p>
      <a-slider :min="0" :max="30" v-model:value="edgeFontSize" @change="changeEdgeFontSize" />

      <br /><br />
      <p>{{ $t('message.ShadowSize') }}</p>
      <a-slider :min="0" :max="10" v-model:value="shadowSize" @change="changeShadowSize" />

      <br /><br />
      <p>{{ $t('message.LineWidth') }}</p>
      <a-slider :min="0" :max="10" v-model:value="lineWidth" @change="changeLineWidth" />

      <br /><br />
      <p>{{ $t('message.LineCurveness') }}</p>
      <a-slider :min="0" :max="1" :step="0.1" v-model:value="lineCurveness" @change="chnageLineCurveness" />

    </a-drawer>
  </div>

</template>

<script>
import { defineComponent, ref, reactive, watch, toRefs, onMounted } from 'vue'
import axios from 'axios'
import VChart from "vue-echarts";

export default defineComponent({
  name: "GraphDetail",
  props: {
    topic: String,
    onlyGraph: {
      default: false,
      type: Boolean
    }
  },
  components: {
    VChart
  },
  setup(props) {
    const API_BASE_URI = axios.defaults.baseURL;

    const simplifyCharacterNote = (note) => {
      if (note) {
        // TODO: Support word wrap and substring more characters
        if (note.length > 6) {
          return note.substring(0, 10) + "...";
        } else {
          return note;
        }
      } else {
        return null;
      }
    };

    const symbolSize = ref(80);
    const labelFontSize = ref(15);
    const edgeFontSize = ref(12);
    const isEnableCharacterWeight = ref(false);
    const shadowSize = ref(2);
    const lineWidth = ref(2);
    const lineCurveness = ref(0);
    const isEnableScale = ref(true);

    const vuechartOption = ref({
      backgroundColor: '#f6f5f3',
      title: {
        show: true,
        text: props.topic,
        textStyle: {
          fontWeight: 700,
          fontSize: 30,
          left: 'center'
        }
      },
      tooltip: {
        trigger: "item",
        formatter: (param) => {
          let template = param.data.name
          if (param.data.name) {
            if (param.data.image_name && isDisplayImage.value) {
              template += '</br>'
              template += `<img src='${API_BASE_URI}/images/${props.topic}/${param.data.image_name}' width="150">`;
            }
            template += '</br>'
            if (param.data.note) {
              template += '<div style="width: 100px">' + simplifyCharacterNote(param.data.note) + '</div>';
            }
          }
          return template;
        }
      },
      series: [
        {
          type: 'graph',
          layout: 'force',
          force: {
            repulsion: [1000, 1200],
            layoutAnimation: true,
            friction: 0.3,
            edgeLength: [100, 130]
          },
          label: {
            show: true,
            fontStyle: 'normal',
            fontSize: labelFontSize.value,
          },
          symbolSize: symbolSize.value,
          itemStyle: {
            shadowColor: '#C0C0C0',
            shadowOffsetX: shadowSize.value,
            shadowOffsetY: shadowSize.value
          },
          roam: isEnableScale.value,
          draggable: true,
          edgeSymbol: ['circle', 'arrow'],
          edgeSymbolSize: [5, 10],
          edgeLabel: {
            show: true,
            formatter: (params) => {
              return params.data.relation;
            },
            fontSize: edgeFontSize,
            color: '#000000'
          },
          cursor: 'pointer',
          emphasis: {
            scale: true,
            focus: 'adjacency'
          },
          lineStyle: {
            color: '#3d3d3f',
            width: lineWidth,
            curveness: lineCurveness
          },
          data: [],
          links: []
        }]
    })

    const isEditGraphDrawerVisible = ref(false);

    const showEditGraphDrawer = () => {
      isEditGraphDrawerVisible.value = true;
    };

    const isCharacterModalVisible = ref(false);
    const currentCharacterModalName = ref("");
    const currentCharacterModalWeight = ref(0.0);
    const currentCharacterModalImageName = ref("");
    const currentModalNote = ref("");

    const handleCharacterModalOk = (e) => {
      isCharacterModalVisible.value = false;
    };

    const handleClickGraph = (params) => {
      isCharacterModalVisible.value = true;
      currentCharacterModalName.value = params.data.name;
      currentCharacterModalWeight.value = params.data.weight;
      currentCharacterModalImageName.value = params.data.image_name;
      //currentModalImagePath.value = params.data.symbol;
      currentModalNote.value = params.data.note;
    }

    // Crop the image for echart graph
    const asyncCropImage = (imgSrc, callback) => {
      const canvas = document.createElement('canvas');
      const contex = canvas.getContext('2d');
      const img = new Image();
      img.crossOrigin = '';

      img.onload = function () {
        const center = {
          x: img.width / 2,
          y: img.height / 2
        }
        var diameter = img.width;
        canvas.width = diameter;
        canvas.height = diameter;
        contex.clearRect(0, 0, diameter, diameter);
        contex.save();
        contex.beginPath();
        const radius = img.width / 2;
        contex.arc(radius, radius, radius, 0, 2 * Math.PI);
        contex.clip();
        contex.drawImage(img, center.x - radius, center.y - radius, diameter, diameter, 0, 0,
          diameter, diameter);
        contex.restore();
        const result = "image://" + canvas.toDataURL('image/png', 0.1);

        callback(result);
      }

      img.src = imgSrc;
    }


    // Copy the original data and only update the data of vuechart
    const updateGraphCharactersData = (charactersInfos) => {
      const series_0 = vuechartOption.value.series[0];
      series_0.data = charactersInfos;
      vuechartOption.value.series[0] = series_0;

      charactersInfos.forEach(function (characterInfo, index, array) {
        if (isEnableCharacterWeight.value) {
          // Update symbol size for character
          charactersInfos[index]["symbolSize"] = characterInfo.weight * 700;
        }

        // Get image and crop for character
        if (characterInfo.image_name && isDisplayImage.value) {
          const imagePath = `${API_BASE_URI}/images/${props.topic}/${characterInfo.image_name}`;
          asyncCropImage(imagePath, function (result) {
            vuechartOption.value.series[0].data[index]["symbol"] = result;
          })
        }
      });
    }

    // Update the graph by reading chooseCharacterCheckboxState
    const updateGraphCharacters = () => {
      if (chooseCharacterCheckboxState.isChooseAllCharacters) {
        // Get all characters
        axios.get(`/api/topics/${props.topic}/characters`).then(response => {
          updateGraphCharactersData(response.data.characters);
        }, response => {
          console.log("Fail to get characters");
        });
      } else if (chooseCharacterCheckboxState.currentChosenCharacterNames.length > 0) {
        // Get characters data from chosen characters
        axios.get(`/api/topics/${props.topic}/characters`, {
          params: {
            chosen_characters_names: chooseCharacterCheckboxState.currentChosenCharacterNames,
          }
        }).then(response => {
          updateGraphCharactersData(response.data.characters);
        }, response => {
          console.log("Fail to get characters");
        });
      } else if (chooseCharacterCheckboxState.currentChosenCharacterNames.length == 0) {
        let series_0 = vuechartOption.value.series[0];
        series_0.data = [];
        vuechartOption.value.series[0] = series_0;
      }
    }

    // Update the characters by accessing chooseGroupCheckboxState
    const updateGroup = () => {
      if (chooseGroupCheckboxState.currentChosenGroupNames.length > 0) {
        // Get characters data from chosen group
        axios.get(`/api/topics/${props.topic}/characters_names`, {
          params: {
            chosen_groups: chooseGroupCheckboxState.currentChosenGroupNames,
          }
        }).then(response => {
          chooseCharacterCheckboxState.currentChosenCharacterNames = [...response.data.characters_names];
        }, response => {
          console.log("Fail to get characters");
        });
      } else {
        chooseCharacterCheckboxState.currentChosenCharacterNames = [];
      }
    }

    let allCharacterNames = ref([]);
    const chooseCharacterCheckboxState = reactive({
      isChooseCharacterIndeterminateState: false,
      isChooseAllCharacters: true,
      currentChosenCharacterNames: [],
    });

    const handleChooseAllCharacters = e => {
      Object.assign(chooseCharacterCheckboxState, {
        currentChosenCharacterNames: e.target.checked ? allCharacterNames.value : [],
        isChooseCharacterIndeterminateState: false,
      });
    };

    watch(() => chooseCharacterCheckboxState.currentChosenCharacterNames, val => {
      chooseCharacterCheckboxState.isChooseCharacterIndeterminateState = !!val.length && val.length < allCharacterNames.value.length;
      chooseCharacterCheckboxState.isChooseAllCharacters = val.length === allCharacterNames.value.length;

      updateGraphCharacters();
    });

    let allGroupNames = ref([]);
    const chooseGroupCheckboxState = reactive({
      isChooseGroupIndeterminateState: false,
      isChooseAllGroups: false,
      currentChosenGroupNames: [],
    });

    const handleChooseAllGroups = (e) => {
      Object.assign(chooseGroupCheckboxState, {
        currentChosenGroupNames: e.target.checked ? allGroupNames.value : [],
        isChooseGroupIndeterminateState: false,
      });
    };

    watch(() => chooseGroupCheckboxState.currentChosenGroupNames, val => {
      chooseGroupCheckboxState.isChooseGroupIndeterminateState = !!val.length && val.length < allGroupNames.value.length;
      chooseGroupCheckboxState.isChooseAllGroups = val.length === allGroupNames.value.length;

      updateGroup();
    });


    const handleEnableCharacterWeight = () => {
      // TODO: If isEnableCharacterWeight is false, no need to handle when changing symbolSize
      let series_0 = vuechartOption.value.series[0];

      // Copy the objects and only reset symbolSize
      let charactersInfos = series_0.data;
      charactersInfos.forEach(function (characterInfo, index, array) {
        if (isEnableCharacterWeight.value) {
          // Update symbol size for characters
          charactersInfos[index]["symbolSize"] = characterInfo.weight * symbolSize.value * 20;
        } else {
          charactersInfos[index]["symbolSize"] = symbolSize.value;
        }

        vuechartOption.value.series[0] = series_0;
      });
    }


    let playGraphTimer = null;
    const playGraphInterval = ref(1000);

    const startPlayGraph = () => {
      const maxCharacterCount = allCharacterNames.value.length;
      let currentCharacterCount = 1;

      // Set chosen characters as empty
      chooseCharacterCheckboxState.currentChosenCharacterNames = [];

      playGraphTimer = setInterval(() => {

        if (currentCharacterCount > maxCharacterCount) {
          stopIncreaseCharacters()
          // Update state of checkbox of isChooseAllCharacters
          chooseCharacterCheckboxState.isChooseAllCharacters = true;
        } else {
          // Select the new character to add
          const addNewCharacterName = allCharacterNames.value[currentCharacterCount - 1];
          chooseCharacterCheckboxState.currentChosenCharacterNames.push(addNewCharacterName);
          updateGraphCharacters();

          currentCharacterCount += 1;
        }
      }, playGraphInterval.value);
    }

    const stopIncreaseCharacters = () => {
      clearInterval(playGraphTimer);
      playGraphTimer = null;
    }

    const handlePlayGraph = () => {
      startPlayGraph();
    }

    const handleStopPlayGraph = () => {
      stopIncreaseCharacters();
    }

    const isShowTitle = ref(true);

    const isDisplayImage = ref(true);

    watch(() => props.topic, (first, second) => {
      // Watch the props and update the graph
      // This used for TopicList componenet which may change topic 
      init();

      // Manually update the title of the graph
      vuechartOption.value.title.text = props.topic;
    });

    const changeSymbolFontSize = () => {
      vuechartOption.value.series[0].label.fontSize = labelFontSize.value;
    }

    const changeEdgeFontSize = () => {
      vuechartOption.value.series[0].edgeSymbol.fontSize = edgeFontSize.value;
    }

    const changeShadowSize = () => {
      vuechartOption.value.series[0].itemStyle.shadowOffsetX = shadowSize.value;
      vuechartOption.value.series[0].itemStyle.shadowOffsetY = shadowSize.value;
    }

    const changeLineWidth = () => {
      vuechartOption.value.series[0].lineStyle.width = lineWidth.value;
    }

    const chnageLineCurveness = () => {
      vuechartOption.value.series[0].lineStyle.curveness = lineCurveness.value;
    }

    const changeIsEnableScale = () => {
      vuechartOption.value.series[0].roam = isEnableScale.value;
    }

    onMounted(() => {
      init();
    })

    const init = () => {

      vuechartOption.value.title.show = isShowTitle.value;

      axios.get(`/api/topics/${props.topic}/characters`).then(response => {
        // The list of character names, used for choose characters to display
        var characterNameList = []
        response.data.characters.forEach(function (characterInfo) {
          characterNameList.push(characterInfo["name"])
        });
        allCharacterNames.value = characterNameList;
        chooseCharacterCheckboxState.currentChosenCharacterNames = characterNameList;

        updateGraphCharacters();
      }, response => {
        console.log(`Fail to get characters for topic: ${props.topic}`);
      });

      axios.get(`/api/topics/${props.topic}/relations`).then(response => {
        vuechartOption.value.series[0].links.push(...response.data.relations);
      }, response => {
        console.log(`Fail to get relations for topic: ${props.topic}`);
      });

      axios.get(`/api/topics/${props.topic}/groups_names`).then(response => {
        allGroupNames.value = response.data.groups_names;
      }, response => {
        console.log(`Fail to get relations for topic: ${props.topic}`);
      });

    }

    return {
      API_BASE_URI,
      init,

      changeSymbolFontSize,
      changeEdgeFontSize,
      changeShadowSize,
      changeLineWidth,
      chnageLineCurveness,
      changeIsEnableScale,

      isShowTitle,
      isDisplayImage,
      symbolSize,
      labelFontSize,
      edgeFontSize,
      shadowSize,
      lineWidth,
      lineCurveness,
      isEnableScale,
      isEnableCharacterWeight,
      handleEnableCharacterWeight,

      vuechartOption,
      handleClickGraph,

      isEditGraphDrawerVisible,
      showEditGraphDrawer,

      isCharacterModalVisible,
      handleCharacterModalOk,
      currentCharacterModalName,
      currentCharacterModalWeight,
      currentCharacterModalImageName,
      currentModalNote,

      ...toRefs(chooseCharacterCheckboxState),
      allCharacterNames,
      handleChooseAllCharacters,

      ...toRefs(chooseGroupCheckboxState),
      allGroupNames,
      handleChooseAllGroups,

      handlePlayGraph,
      handleStopPlayGraph,
      playGraphInterval,


    }

  }
})

</script>

<style scoped>
.chart {
  height: 800px;
}
</style>