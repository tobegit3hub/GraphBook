
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

    const dynamicNodeWeight = false;

    let increase_nodes_timer = null;
    let current_node_count = 0;

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

    const startIncreaseNodes = () => {
      const max_node_count = 9;
      const add_node_interval = 100;

      this.increase_nodes_timer = setInterval(() => {
        console.log("Current node count: " + this.current_node_count)

        if (this.current_node_count >= max_node_count) {
          this.stopIncreaseNodes()
        } else {
          this.option.series[0].data.push(this.nodes[this.current_node_count]);
          this.current_node_count += 1;
        }
      }, add_node_interval);

    }

    const stopIncreaseNodes = () => {
      clearInterval(this.increase_nodes_timer);
      this.increase_nodes_timer = null
      console.log("Stop increase nodes timer")
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
    const updateGraphNodesData = (nodes) => {
      let series_0 = vuechartOption.value.series[0];
      series_0.data = nodes;
      vuechartOption.value.series[0] = series_0;

      nodes.forEach(function (node, index, array) {
        if (dynamicNodeWeight) {
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
          console.log("tobetest");
          console.log(response.data.nodes);
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
      isChooseAllGroups: true,
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

      // TODO: we choose all groups by default but it may not get all node at start
      updateGroup();
    });

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
        chooseGroupCheckboxState.currentChosenGroupNames = allGroupNames.value;
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
      handleChooseAllGroups
    }

  }
})

</script>

<style scoped>
.chart {
  height: 800px;
}
</style>