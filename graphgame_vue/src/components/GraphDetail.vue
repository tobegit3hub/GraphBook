
<template>

  <h1>GraphDetail</h1>

  <v-chart class="chart" :option="option" />

</template>

<script>
import VChart, { THEME_KEY } from "vue-echarts";
import axios from 'axios'

import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from "echarts/components";

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

export default {
  name: "GraphDetail",
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "dark"
  },
  data() {
    return {
      nodes: [],
      links: [],

      increase_nodes_timer: null,
      current_node_count: 0,

      option: {
        backgroundColor: '#f6f5f3',
        title: {
          text: "cyberpunk_edgerunner",
          textStyle: {
            color: '#368cbf',
            fontWeight: 700,
            fontSize: 30,
            left: 'center'
          }
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
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
          roam: true, //开启鼠标平移及缩放
          draggable: true, //节点是否支持鼠标拖拽。
          edgeSymbol: ['circle', 'arrow'],//两节点连线的样式
          edgeSymbolSize: [5, 10],
          edgeLabel: {
            show: true,
            formatter: (params) => {
              return params.data.relation;
            },
            textStyle: {
              fontSize: 12,
              color: '#000000'
            }
          },
          cursor: 'pointer', //鼠标悬浮时在图形元素上时鼠标的样式
          labelLayout: {
            moveOverlap: 'shiftX', //标签重叠时，挪动标签防止重叠
            draggable: true //节点标签是否允许鼠标拖拽定位
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
          roam: true,
          data: [],
          links: []
      }]
    }
    };
  },
  methods: {

    update_graph() {
      axios.get('http://127.0.0.1:7788/api/cyberpunk_edgerunner/nodes', {
        params: {
          num: this.current_node_count
        }
      }).then(response => {
          this.nodes = response.data.nodes;
          console.log("Get nodes: " + this.nodes);
          this.option.series[0].data.push(...this.nodes)
      }, response => {
          console.log("Fail to get nodes");
      }); 

      axios.get('http://127.0.0.1:7788/api/cyberpunk_edgerunner/edges').then(response => {
          this.edges = response.data.edges;
          console.log("Get edges: " + this.edges);
          this.option.series[0].links.push(...this.edges)
      }, response => {
          console.log("Fail to get edges");
      });
    },
    
    start_increase_nodes() {
      const max_node_count = 9;
      const add_node_interval = 100;

      this.increase_nodes_timer = setInterval(() => {
          console.log("Current node count: " + this.current_node_count)

          if (this.current_node_count >= max_node_count) {
            this.stop_increase_nodes()
          } else {
            this.option.series[0].data.push(this.nodes[this.current_node_count]);
            this.current_node_count += 1;
          }
      }, add_node_interval);

    },

    stop_increase_nodes() {
      clearInterval(this.increase_nodes_timer);
      this.increase_nodes_timer = null
      console.log("Stop increase nodes timer")
    }
    
  },
  mounted () {

    axios.get('http://127.0.0.1:7788/api/cyberpunk_edgerunner/nodes', {
      params: {
        num: -1
      }
    }).then(response => {
        this.nodes = response.data.nodes;
        console.log("Get nodes: " + this.nodes);
        // Do not add all nodes at once
        this.option.series[0].data.push(...this.nodes)
    }, response => {
        console.log("Fail to get nodes");
    }); 

    axios.get('http://127.0.0.1:7788/api/cyberpunk_edgerunner/edges').then(response => {
        this.edges = response.data.edges;
        console.log("Get edges: " + this.edges);
        this.option.series[0].links.push(...this.edges)
    }, response => {
        console.log("Fail to get edges");
    });

    //this.start_increase_nodes();
  }
};

</script>

<style scoped>
.chart {
  height: 800px;
}
</style>