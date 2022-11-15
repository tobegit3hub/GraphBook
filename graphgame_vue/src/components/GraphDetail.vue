
<template>

  <v-chart class="chart" :option="vuechartOption" />

  <h3>Characters:</h3>
  <div>
    <a-checkbox v-model:checked="isChooseAllUsers" :indeterminate="isChooseUserIndeterminateState"
      @change="handleChooseAllUsers">
      Choose all
    </a-checkbox>
  </div>
  <a-checkbox-group v-model:value="currentChosenUserNames" :options="allNodeNames" />

  <h3>Groups:</h3>
  <div>
    <a-checkbox v-model:checked="isChooseAllGroups" :indeterminate="isChooseGroupIndeterminateState"
      @change="handleChooseAllGroups">
      Choose all
    </a-checkbox>
  </div>
  <a-checkbox-group v-model:value="currentChosenGroupNames" :options="allGroupNames" />

  <h3>Resize characters with weight:</h3>
  <div>
    <a-row>
      <a-col :span="8">
        <a-slider v-model:value="nodeWeightFactor" @change="handleEnableNodeWeight" />
      </a-col>
      <a-col :span="8">
        <a-switch v-model:checked="isEnableNodeWeight" @change="handleEnableNodeWeight" />
      </a-col>
    </a-row>
  </div>

  <h3>Play graph animation:</h3>
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



</template>

<script>
import { defineComponent, ref, reactive, watch, toRefs, onMounted } from 'vue'

import axios from 'axios'

import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

export default defineComponent({
  name: "GraphDetail",
  props: {
    dbName: String,
  },
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "dark"
  },
  setup(props) {

    const simplifyNodeNote = (note) => {
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
        text: props.dbName,
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
          if (param.data.display_name) {
            template = param.data.display_name
          }
          // TODO: Display image, handle image not found
          if (param.data.name) {
            template += '</br></br>'
            template += `<img src='http://localhost:7788/images/${props.dbName}/${param.data.name}.png' width="100">`;
            template += '</br></br>'
            if (param.data.note) {
              template += '<div style="width: 100px">' + simplifyNodeNote(param.data.note) + '</div>';
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
    const updateGraphNodesData = (nodes) => {
      let series_0 = vuechartOption.value.series[0];
      series_0.data = nodes;
      vuechartOption.value.series[0] = series_0;

      nodes.forEach(function (node, index, array) {
        if (isEnableNodeWeight.value) {
          // Update symbol size for node
          nodes[index]["symbolSize"] = node.weight * 700;
        }

        // Get image and crop for node
        const imagePath = `http://localhost:7788/images/${props.dbName}/${node.name}.png`;
        asyncCropImage(imagePath, function (result) {
          // TODO: Handle if can not load image
          vuechartOption.value.series[0].data[index]["symbol"] = result;
        })
      });
    }

    // Update the graph by reading chooseUserCheckboxState
    const updateGraphNodes = () => {
      if (chooseUserCheckboxState.isChooseAllUsers) {
        // Get all nodes
        axios.get(`http://127.0.0.1:7788/api/${props.dbName}/nodes`).then(response => {
          updateGraphNodesData(response.data.nodes);
        }, response => {
          console.log("Fail to get nodes");
        });
      } else if (chooseUserCheckboxState.currentChosenUserNames.length > 0) {
        // Get nodes data from chosen nodes
        axios.get(`http://127.0.0.1:7788/api/${props.dbName}/nodes`, {
          params: {
            chosen_nodes: chooseUserCheckboxState.currentChosenUserNames,
          }
        }).then(response => {
          updateGraphNodesData(response.data.nodes);
        }, response => {
          console.log("Fail to get nodes");
        });
      } else if (chooseUserCheckboxState.currentChosenUserNames.length == 0) {
        let series_0 = vuechartOption.value.series[0];
        series_0.data = [];
        vuechartOption.value.series[0] = series_0;
      }
    }

    // Update the nodes by accessing chooseGroupCheckboxState
    const updateGroup = () => {

      if (chooseGroupCheckboxState.currentChosenGroupNames.length > 0) {
        // Get nodes data from chosen group
        axios.get(`http://127.0.0.1:7788/api/${props.dbName}/node_names`, {
          params: {
            chosen_groups: chooseGroupCheckboxState.currentChosenGroupNames,
          }
        }).then(response => {
          chooseUserCheckboxState.currentChosenUserNames = [...response.data.nodes];
        }, response => {
          console.log("Fail to get nodes");
        });
      } else {
        chooseUserCheckboxState.currentChosenUserNames = [];
      }
    }

    let allNodeNames = ref([]);
    const chooseUserCheckboxState = reactive({
      isChooseUserIndeterminateState: false,
      isChooseAllUsers: true,
      currentChosenUserNames: [],
    });

    const handleChooseAllUsers = e => {
      Object.assign(chooseUserCheckboxState, {
        currentChosenUserNames: e.target.checked ? allNodeNames.value : [],
        isChooseUserIndeterminateState: false,
      });
    };

    watch(() => chooseUserCheckboxState.currentChosenUserNames, val => {
      chooseUserCheckboxState.isChooseUserIndeterminateState = !!val.length && val.length < allNodeNames.value.length;
      chooseUserCheckboxState.isChooseAllUsers = val.length === allNodeNames.value.length;
      updateGraphNodes();
    });

    let allGroupNames = ref([]);
    const chooseGroupCheckboxState = reactive({
      isChooseGroupIndeterminateState: false,
      isChooseAllGroups: false,
      currentChosenGroupNames: [],
    });

    const handleChooseAllGroups = e => {
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


    const nodeWeightFactor = ref(50);
    const isEnableNodeWeight = ref(false);

    const handleEnableNodeWeight = () => {
      // TODO: If isEnableNodeWeight is false, no need to handle when changing nodeWeightFactor

      let series_0 = vuechartOption.value.series[0];

      // Copy the objects and only reset symbolSize
      let nodes = series_0.data;
      nodes.forEach(function (node, index, array) {
        if (isEnableNodeWeight.value) {
          // Update symbol size for node
          nodes[index]["symbolSize"] = node.weight * nodeWeightFactor.value * 20;
        } else {
          nodes[index]["symbolSize"] = null;
        }

        vuechartOption.value.series[0] = series_0;
      });
    }


    let playGraphTimer = null;
    const playGraphInterval = ref(1000);

    const startPlayGraph = () => {
      const maxNodeCount = allNodeNames.value.length;
      let currentNodeCount = 1;

      // Set chosen users as empty
      chooseUserCheckboxState.currentChosenUserNames = [];

      playGraphTimer = setInterval(() => {

        if (currentNodeCount > maxNodeCount) {
          stopIncreaseNodes()
        } else {
          // Select the new node to add
          const addNewNodeName = allNodeNames.value[currentNodeCount - 1];
          chooseUserCheckboxState.currentChosenUserNames.push(addNewNodeName);
          updateGraphNodes();

          currentNodeCount += 1;
        }
      }, playGraphInterval.value);
    }

    const stopIncreaseNodes = () => {
      clearInterval(playGraphTimer);
      playGraphTimer = null;
    }

    const handlePlayGraph = () => {
      startPlayGraph();
    }

    onMounted(() => {
      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/nodes`, {
        params: {
          num: -1
        }
      }).then(response => {
        // The list of node names, used for choose users to display
        var nodeNameList = []
        response.data.nodes.forEach(function (node) {
          nodeNameList.push(node["name"])
        });
        allNodeNames.value = nodeNameList;
        chooseUserCheckboxState.currentChosenUserNames = nodeNameList;

        updateGraphNodes();
      }, response => {
        console.log("Fail to get nodes");
      });

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/edges`).then(response => {
        vuechartOption.value.series[0].links.push(...response.data.edges);
      }, response => {
        console.log("Fail to get edges");
      });

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/group_names`).then(response => {
        allGroupNames.value = response.data.group_names;
      }, response => {
        console.log("Fail to get edges");
      });

    })

    return {
      vuechartOption,

      ...toRefs(chooseUserCheckboxState),
      allNodeNames,
      handleChooseAllUsers,

      ...toRefs(chooseGroupCheckboxState),
      allGroupNames,
      handleChooseAllGroups,

      nodeWeightFactor,
      isEnableNodeWeight,
      handleEnableNodeWeight,

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