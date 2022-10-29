
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
      edges: [],

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
    },
    
    
    getImgData(imgSrc) {
 
      var fun = function (resolve) {
          const canvas = document.createElement('canvas');
          const contex = canvas.getContext('2d');
          const img = new Image();
          img.crossOrigin = '';

          img.onload = function () {
              //设置图形宽高比例
              var center = {
                  x: img.width / 2,
                  y: img.height / 2
              }
              var diameter = img.width;//半径
              canvas.width = diameter;
              canvas.height = diameter;
              contex.clearRect(0, 0, diameter, diameter);
              contex.save();
              contex.beginPath();
              var radius = img.width / 2;
              contex.arc(radius, radius, radius, 0, 2 * Math.PI); //画出圆
              contex.clip(); //裁剪上面的圆形
              contex.drawImage(img, center.x - radius, center.y - radius, diameter, diameter, 0, 0,
                  diameter, diameter); // 在刚刚裁剪的园上画图
              contex.restore(); // 还原状态
              resolve(canvas.toDataURL('image/png', 1))
          }
          img.src = imgSrc;
      }

      var promise = new Promise(fun);

      return promise
    },

    getImgData2(imgSrc, callback) {
          const canvas = document.createElement('canvas');
          const contex = canvas.getContext('2d');
          const img = new Image();
          img.crossOrigin = '';

          img.onload = function() {

            //设置图形宽高比例
            const center = {
                x: img.width / 2,
                y: img.height / 2
            }
            var diameter = img.width;//半径
            canvas.width = diameter;
            canvas.height = diameter;
            contex.clearRect(0, 0, diameter, diameter);
            contex.save();
            contex.beginPath();    
            const radius = img.width / 2;
            contex.arc(radius, radius, radius, 0, 2 * Math.PI); //画出圆
            contex.clip(); //裁剪上面的圆形
            contex.drawImage(img, center.x - radius, center.y - radius, diameter, diameter, 0, 0,
                diameter, diameter); // 在刚刚裁剪的园上画图
            contex.restore(); // 还原状态
            const result =  "image://" + canvas.toDataURL('image/png', 0.1);

            callback(result);

          }

          img.src = imgSrc;
      }
  },

  update_image_func(images) {
    console.log("call update image func");

     var symbol;
      for (var i = 0; i < images.length; i++) {
                    var img = "image://" + images[i];
                    console.log(img);
                    //androidMap[i].symbol = img;
                    response.data.nodes[0]["symbol"] = img;
                    symbol = img;
                    

                }

                response.data.nodes[0]["symbol"] = symbol;

                console.log('abcdefg');
                console.log(symbol)

                this.option.series[0].data.push(...response.data.nodes);
        
    },

    my_callback(that, result){ 
      console.log("Get callback result");
      console.log(result);
      response.data.nodes[0]["symbol"] = result;
      console.log(that.nodes);
      console.log(that.option);
//      this.option.series[0].data.push(...response.data.nodes);
//      response.data.nodes[0]["symbol"] = 'image://data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7';
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
//        this.option.series[0].data.push(...response.data.nodes);

    const test_image_path = "http://localhost:7788/images/cyberpunk_edgerunner/david.png";

    const vue_this = this;
    this.getImgData2(test_image_path, function(result){ 
      console.log("Get callback result");
      console.log(result);
      response.data.nodes[0]["symbol"] = result;

      vue_this.option.series[0].data.push(...response.data.nodes);
    })

      //this.option.series[0].data.push(...response.data.nodes);

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