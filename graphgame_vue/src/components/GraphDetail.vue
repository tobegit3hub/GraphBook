
<template>

  <h1>
    GraphDetail
  </h1>

  <v-chart class="chart" :option="option" />

</template>


<script>

import VChart, { THEME_KEY } from "vue-echarts";
import { ref, defineComponent } from "vue";
import { onMounted } from '@vue/runtime-core';

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

export default defineComponent({
  name: "GraphDetail",
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "dark"
  },
  setup: () => {

    onMounted(async () => {
      self.nodes = await fetch("http://127.0.0.1:7788/api/cyberpunk_edgerunner/nodes")
        .then(res => res.json()).then(data => data.nodes);
      console.log("Get nodes: " + self.nodes);

      self.edges = await fetch("http://127.0.0.1:7788/api/cyberpunk_edgerunner/edges")
        .then(res => res.json()).then(data => data.edges);
      console.log("Get edges: " + self.edges);

    });

    const option = ref({
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
        legendHoverLink: true,  // 可以点击图例来隐藏一个组
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
          fontSize: 12,
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
        data: self.nodes, 
        links: self.edges
    }
    ]
    });

    return { option };
  }
});

</script>

<style scoped>
.chart {
  height: 800px;
}
</style>