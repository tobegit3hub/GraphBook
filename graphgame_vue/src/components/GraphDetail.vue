
<template>

  <h1>GraphDetail</h1>

  <v-chart class="chart" :option="vuechartOption" />

  <h3>Groups:</h3>
  <ul>
    <li>
      <button @click="changeGroup('')">All Groups</button>
    </li>
    <li v-for="group_name in group_names">
      <button @click="changeGroup(group_name)">{{ group_name }}</button>
    </li>
  </ul>

</template>

<script>
import { defineComponent, ref, onMounted} from 'vue'

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
  setup (props) {

      const dynamicNodeWeight = false;

      let nodes = ref([]);
      let edges = ref([]);
      let group_names = ref([]);
      let current_group_name = ref("");

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
              if (param.data.display_name) {
                return param.data.display_name;
              } else {
                return param.data.name;
              }
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

  const asyncCropImage = (imgSrc, callback) => {
        const canvas = document.createElement('canvas');
        const contex = canvas.getContext('2d');
        const img = new Image();
        img.crossOrigin = '';

        img.onload = function() {
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
          const result =  "image://" + canvas.toDataURL('image/png', 0.1);

          callback(result);
        }

        img.src = imgSrc;
    }

    const changeGroup = (group_name) => {
      console.log("Change group: " + group_name);
      current_group_name.value = group_name;


      updateNodes();
    }

    const updateNodes = () => {
      console.log("Call update nodes");

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/nodes`, {
        params: {
          num: -1,
          group: current_group_name.value
        }
      }).then(response => {
        nodes.value = response.data.nodes;

        // Reset nodes data
        // TODO: Update the image symbol as well
        let series_0 = vuechartOption.value.series[0];
        series_0.data = response.data.nodes;
        vuechartOption.value.series[0] = series_0;

      }, response => {
          console.log("Fail to get nodes");
      }); 
    }

    onMounted(() => {

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/nodes`, {
        params: {
          num: -1
        }
      }).then(response => {
        nodes.value = response.data.nodes;

        nodes.value.forEach(function(node, index, array) {
          if (dynamicNodeWeight) {
            // Update symbol size for node
            response.data.nodes[index]["symbolSize"] = node.weight * 700;
          }
          
          // Get image and crop for node
          const test_image_path = `http://localhost:7788/images/${props.dbName}/${node.name}.png`;
          asyncCropImage(test_image_path, function(result){
            // TODO: Handle if can not load image
            vuechartOption.value.series[0].data[index]["symbol"] = result;
          })
        });

        // Comment out if do not add all nodes at once
        vuechartOption.value.series[0].data.push(...response.data.nodes);

      }, response => {
          console.log("Fail to get nodes");
      }); 

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/edges`).then(response => {
          edges.value = response.data.edges;
          vuechartOption.value.series[0].links.push(...response.data.edges);
      }, response => {
          console.log("Fail to get edges");
      });

      axios.get(`http://127.0.0.1:7788/api/${props.dbName}/group_names`).then(response => {
          group_names.value = response.data.group_names;
      }, response => {
          console.log("Fail to get edges");
      });

      //this.startIncreaseNodes();
    })

    return {
      vuechartOption,
      nodes,
      edges,
      group_names,
      current_group_name,
      changeGroup
    }

  }
})

</script>

<style scoped>
.chart {
  height: 800px;
}
</style>