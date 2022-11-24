
<template>

  <div v-if="character">
    <h1>Character {{ character.name }}</h1>

    <p>Name: {{ character.name }}</p>
    <p>Weight: {{ character.weight }}</p>
    <p>Note: {{ character.note }}</p>
    <a-image :src="`${API_BASE_URI}/images/${topic}/${character.image_name}`" width="100px" />
  </div>

  <h2>Character association:</h2>
  <a-switch v-model:checked="isUpstream" checked-children="Upstream" un-checked-children="Downstream"
    @change="handleUpstreamSwitchChange" />
  <v-chart class="chart" :option="vuechartOption" @dblclick="handleDoubleClickGraph" />
</template>

<script>
import { defineComponent, ref, onMounted, watch } from 'vue'
import axios from 'axios'
import VChart from "vue-echarts";

export default defineComponent({
  name: "CharacterDetail",
  props: {
    topic: String,
    character_name: String,
  },
  components: {
    VChart
  },
  setup(props) {
    const API_BASE_URI = axios.defaults.baseURL;

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
          orient: 'BT',
          data: [],
          leaves: {
            label: {
              verticalAlign: 'middle',
            }
          },
          emphasis: {
            focus: 'descendant'
          },
          expandAndCollapse: false,
          animationDuration: 550,
          animationDurationUpdate: 750
        }]
    })

    const isUpstream = ref(true)
    const handleUpstreamSwitchChange = () => {
      if (isUpstream.value) {
        vuechartOption.value.series[0].data[0] = upstream_data;
        vuechartOption.value.series[0]["orient"] = "BT";
      } else {
        vuechartOption.value.series[0].data[0] = downstream_data;
        vuechartOption.value.series[0]["orient"] = "TB";
      }
    }

    // TODO: Support modal when double click
    const isShowModal = ref(false);

    const handleDoubleClickGraph = (params) => {
      isShowModal.value = true;
    }

    watch(() => props.topic, (first, second) => {
      init();
    });
    watch(() => props.character_name, (first, second) => {
      init();
    });

    const init = () => {
      axios.get(`/api/topics/${props.topic}/characters/${props.character_name}`)
        .then(response => {
          character.value = response.data.character;

          upstream_data = {
            "name": character.value.name, "children": [], "symbolSize": 100,
            "symbol": `image://${API_BASE_URI}/images/${props.topic}/${character.value.image_name}`
          }

          response.data.upstream_characters.forEach(function (upstream_character, index) {
            upstream_data["children"].push({
              "name": upstream_character.name,
              "symbolSize": 100,
              "symbol": `image://${API_BASE_URI}/images/${props.topic}/${upstream_character.image_name}`
            });
          })

          downstream_data = {
            "name": character.value.name, "children": [], "symbolSize": 100,
            "symbol": `image://${API_BASE_URI}/images/${props.topic}/${character.value.image_name}`
          }

          response.data.downstream_characters.forEach(function (downstream_character, index) {
            downstream_data["children"].push({
              "name": downstream_character.name,
              "symbolSize": 100,
              "symbol": `image://${API_BASE_URI}/images/${props.topic}/${downstream_character.image_name}`
            });
          })

          vuechartOption.value.series[0].data[0] = upstream_data;
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      init();
    })

    return {
      API_BASE_URI,

      character,
      vuechartOption,
      handleDoubleClickGraph,
      isUpstream,
      handleUpstreamSwitchChange,
      isShowModal
    }
  }
})
</script>

<style scoped>
.chart {
  height: 800px;
}
</style>