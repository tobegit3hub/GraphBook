
<template>

  <h2>Character detail:</h2>
  <div v-if="character">
    <p>Name: {{ character.name}}</p>
    <p>Weight: {{character.weight}}</p>
    <p>Note: {{character.note}}</p>
    <a-image :src="'http://localhost:7788/images/' + topic + '/' + character.name + '.png'" width="30px"/>
  </div>

  <h2>Character association:</h2>
  <a-switch v-model:checked="isUpstream" checked-children="Upstream" un-checked-children="Downstream" @change="handleUpstreamSwitchChange" />
  <v-chart class="chart" :option="vuechartOption" />

</template>

<script>
import { defineComponent, ref, onMounted} from 'vue'
import axios from 'axios'
import VChart from "vue-echarts";

export default defineComponent({
  name: "CharacterDetail",
  props: {
    topic: String,
    name: String,
  },
  components: {
    VChart
  },
  setup (props) {
   
    const character = ref();
    let upstream_data = {};
    let downstream_data = {};

    const vuechartOption = ref({
      tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove'
      },
      series: [
        {
          type: 'tree',
          orient: 'RL',
          data: [],
          leaves: {
            label: {
              position: 'left',
              verticalAlign: 'middle',
              align: 'right'
            }
          },
          emphasis: {
            focus: 'descendant'
          },
          expandAndCollapse: true,
          animationDuration: 550,
          animationDurationUpdate: 750
        }]
    })

    const isUpstream = ref(true)
    const handleUpstreamSwitchChange = () => {
      if (isUpstream.value) {
        vuechartOption.value.series[0].data[0] = upstream_data;
        vuechartOption.value.series[0]["orient"] = "RL";
        vuechartOption.value.series[0]["leaves"]["label"]["position"] = "left";
        vuechartOption.value.series[0]["leaves"]["label"]["align"] = "right";
      } else {
        vuechartOption.value.series[0].data[0] = downstream_data;
        vuechartOption.value.series[0]["orient"] = "LR";
        vuechartOption.value.series[0]["leaves"]["label"]["position"] = "right";
        vuechartOption.value.series[0]["leaves"]["label"]["align"] = "left";
      }
    }

    onMounted(() => {
      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/characters/${props.name}`)
        .then(response => {
          character.value = response.data.character;

          upstream_data = {"name": character.value.name, "children": [], "symbolSize": 100,
            "symbol": `image://http://localhost:7788/images/${props.topic}/${character.value.name}.png`}

          response.data.upstream_characters.forEach(function (upstream_character, index) {
            console.log(`image://http://localhost:7788/images/${props.topic}/${upstream_character.name}.png`);
            upstream_data["children"].push({
              "name": upstream_character.name, 
              "symbolSize": 100,
              "symbol": `image://http://localhost:7788/images/${props.topic}/${upstream_character.name}.png`
            });
          })

          downstream_data = {"name": character.value.name, "children": [], "symbolSize": 100,
            "symbol": `image://http://localhost:7788/images/${props.topic}/${character.value.name}.png`}

          response.data.downstream_characters.forEach(function (downstream_character, index) {
            downstream_data["children"].push({
              "name": downstream_character.name, 
              "symbolSize": 100,
              "symbol": `image://http://localhost:7788/images/${props.topic}/${downstream_character.name}.png`
            });
          })

          vuechartOption.value.series[0].data[0] = upstream_data;
        })
        .catch(error => {
          console.log(error);
        });        
    })

    return {
      character,
      vuechartOption,
      isUpstream,
      handleUpstreamSwitchChange
    }
  }
})
</script>

<style scoped>
.chart {
  height: 800px;
}
</style>