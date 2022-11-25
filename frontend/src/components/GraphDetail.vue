
<template>

  <br />
  <v-chart class="chart" :option="vuechartOption" @dblclick="handleDoubleClickGraph" />

  <div v-show="!onlyGraph">
    <a-modal v-model:visible="isCharacterModalVisible" :title="currentCharacterModalName" @ok="handleCharacterModalOk">
      <p>Name: <router-link :to='`/topics/${topic}/characters/${currentCharacterModalName}`'>{{ currentCharacterModalName }}</router-link></p>
      <p>Weight: {{ currentCharacterModalWeight }}</p>
      <a-image v-if="!currentCharacterModalImageName===''" :src="`${API_BASE_URI}/images/${topic}/${currentCharacterModalImageName}`" />
      <br/><br/>
      <p>Note:</p>
      <p>{{ currentModalNote }}</p>
    </a-modal>

    <br />

    <h2>Characters</h2>
    <div>
      <a-checkbox v-model:checked="isChooseAllCharacters" :indeterminate="isChooseCharacterIndeterminateState"
        @change="handleChooseAllCharacters">
        Choose all
      </a-checkbox>
    </div>
    <a-checkbox-group v-model:value="currentChosenCharacterNames" :options="allCharacterNames" />

    <br /><br />
    <h2>Groups</h2>
    <div>
      <a-checkbox v-model:checked="isChooseAllGroups" :indeterminate="isChooseGroupIndeterminateState"
        @change="handleChooseAllGroups">
        Choose all
      </a-checkbox>
    </div>
    <a-checkbox-group v-model:value="currentChosenGroupNames" :options="allGroupNames" />

    <br /><br />
    <h2>Resize images with weight:</h2>
    <div>
      <a-row>
        <a-col :span="8">
          <a-slider v-model:value="characterWeightFactor" @change="handleEnableCharacterWeight" />
        </a-col>
        <a-col :span="8">
          <a-switch v-model:checked="isEnableCharacterWeight" @change="handleEnableCharacterWeight" />
        </a-col>
      </a-row>
    </div>

    <br />
    <h2>Play graph animation</h2>
    <div>
      <a-row>
        <a-col :span="8">
          <a-slider v-model:value="playGraphInterval" :min="10" :max="10000" />
        </a-col>
        <a-col :span="8">
          <a-button type="primary" @click="handlePlayGraph">Play Graph</a-button>
        </a-col>
      </a-row>
    </div>
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
          return note.substring(0, 6) + "...";
        } else {
          return note;
        }
      } else {
        return null;
      }
    };

    const vuechartOption = ref({
      backgroundColor: '#f6f5f3',
      title: {
        text: props.topic,
        textStyle: {
          color: '#368cbf',
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
            if (!param.data.image_name==="") {
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
          type: 'graph', // 类型设置为关系图
          layout: 'force',
          force: {
            repulsion: [1000, 1200], //每个节点之间的斥力因子，越大离的越远
            layoutAnimation: true,
            friction: 0.3, //刷新时节点的移动速度，越大越快，0 - 1 之间
            edgeLength: [100, 130] //两节点之间的距离
          },
          label: {
            show: true, // 节点圆盘上的文字
            fontStyle: 'italic', //文字风格，normal，italic，oblique 三种可选
            fontSize: 16,
            color: '#000000',
          },
          symbolSize: 60, //全局节点尺寸
          itemStyle: {  // 给节点加上阴影，显着立体
            shadowColor: '#C0C0C0',
            shadowOffsetX: 2,
            shadowOffsetY: 2
          },
          //让节点可以通过鼠标拖拽和移动的设置
          roam: false, //开启鼠标平移及缩放
          draggable: true, //节点是否支持鼠标拖拽。
          edgeSymbol: ['circle', 'arrow'],//两节点连线的样式
          edgeSymbolSize: [5, 10],
          edgeLabel: {
            show: true,
            formatter: (params) => {
              return params.data.relation;
            },
            fontSize: 12,
            color: '#000000'
          },
          cursor: 'pointer', //鼠标悬浮时在图形元素上时鼠标的样式
          labelLayout: {
            moveOverlap: 'shiftX', //标签重叠时，挪动标签防止重叠
            draggable: false //节点标签是否允许鼠标拖拽定位
          },
          emphasis: {
            scale: true, //节点放大效果
            focus: 'adjacency'
          },
          lineStyle: {
            color: '#3d3d3f',
            width: 2,
            curveness: 0 //节点连线的曲率，0-1 越大越弯。
          },
          data: [],
          links: []
        }]
    })

    const isCharacterModalVisible = ref(false);
    const currentCharacterModalName = ref("");
    const currentCharacterModalWeight = ref(0.0);
    const currentCharacterModalImageName = ref("");
    const currentModalNote = ref("");

    const handleCharacterModalOk = (e) => {
      isCharacterModalVisible.value = false;
    };

    const handleDoubleClickGraph = (params) => {
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
      let series_0 = vuechartOption.value.series[0];
      series_0.data = charactersInfos;
      vuechartOption.value.series[0] = series_0;

      charactersInfos.forEach(function (characterInfo, index, array) {
        if (isEnableCharacterWeight.value) {
          // Update symbol size for character
          charactersInfos[index]["symbolSize"] = characterInfo.weight * 700;
        }

        // Get image and crop for character
        if (!characterInfo.image_name==="") {
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


    const characterWeightFactor = ref(50);
    const isEnableCharacterWeight = ref(false);

    const handleEnableCharacterWeight = () => {
      // TODO: If isEnableCharacterWeight is false, no need to handle when changing characterWeightFactor

      let series_0 = vuechartOption.value.series[0];

      // Copy the objects and only reset symbolSize
      let charactersInfos = series_0.data;
      charactersInfos.forEach(function (characterInfo, index, array) {
        if (isEnableCharacterWeight.value) {
          // Update symbol size for characters
          charactersInfos[index]["symbolSize"] = characterInfo.weight * characterWeightFactor.value * 20;
        } else {
          charactersInfos[index]["symbolSize"] = null;
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

    watch(() => props.topic, (first, second) => {
      // Watch the props and update the graph
      // This used for TopicList componenet which may change topic 
      init();

      // Manually update the title of the graph
      vuechartOption.value.title.text = props.topic;
    });

    onMounted(() => {
      init();
    })

    const init = () => {

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

      vuechartOption,
      handleDoubleClickGraph,
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

      characterWeightFactor,
      isEnableCharacterWeight,
      handleEnableCharacterWeight,

      handlePlayGraph,
      playGraphInterval
    }

  }
})

</script>

<style scoped>
.chart {
  height: 800px;
}
</style>