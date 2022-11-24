
<template>

  <div v-if="character">

    <a-modal v-model:visible="isRelatioinModalVisible" title="Relation" width="1000px" @ok="handleRelationModalOk">

    <a-row>
        <a-col :span="8">
          <h1>{{ character.name }}</h1>
          <a-image :src="`${API_BASE_URI}/images/${topic}/${character.image_name}`" />
        </a-col>
        <a-col :span="8">
          <div style="padding: 200px 30px">
            <h3>{{ relationCharacterData.relation }}</h3>

            <div v-if="isUpstream">
              <h1>&lt;---------------</h1>
            </div>
            <div v-if="!isUpstream">
              <h1>---------------&gt;</h1>
            </div>

            <h3>{{ relationCharacterData.relation_note }}</h3>
          </div>
        </a-col>
        <a-col :span="8">
          <h1> {{ relationCharacterData.name }} </h1>
          <a-image :src="`${API_BASE_URI}/images/${topic}/${relationCharacterData.image_name}`" />
        </a-col>
      </a-row>

    </a-modal>
    
    <h1>Character {{ character.name }}</h1>

    <p>Name: {{ character.name }}</p>
    <p>Weight: {{ character.weight }}</p>
    <p>Note: {{ character.note }}</p>
    <a-image :src="`${API_BASE_URI}/images/${topic}/${character.image_name}`" width="100px" />
  </div>

  <h2>Character association:</h2>
  <a-switch v-model:checked="isUpstream" checked-children="Upstream" un-checked-children="Downstream"
    @change="handleUpstreamSwitchChange" />
  <v-chart class="chart" :option="vuechartOption" @click="handleClickCharacter" />
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

    const isRelatioinModalVisible = ref(false);
    const relationCharacterData = ref();

    const handleRelationModalOk = (e) => {
      isRelatioinModalVisible.value = false;
    };

    const handleClickCharacter = (params) => {

      if (params.data.name != character.value.name) {
        isRelatioinModalVisible.value = true;
        relationCharacterData.value = {
          "name": params.data.name,
          "image_name": params.data.image_name,
          "relation": params.data.relation,
          "relation_note": params.data.relation_note
        }
      }

    }

    watch(() => props.topic, (first, second) => {
      init();
    });
    watch(() => props.character_name, (first, second) => {
      init();
    });

    const init = () => {
      axios.get(`/api/topics/${props.topic}/characters/${props.character_name}/relations`)
        .then(response => {
          character.value = response.data.character;

          upstream_data = {
            "name": character.value.name, "children": [], "symbolSize": 100,
            "symbol": `image://${API_BASE_URI}/images/${props.topic}/${character.value.image_name}`
          }

          response.data.upstream_characters_and_relations.forEach(function (upstream_character_and_relation, index) {
            upstream_data["children"].push({
              "name": upstream_character_and_relation.name,
              "symbolSize": 100,
              "symbol": `image://${API_BASE_URI}/images/${props.topic}/${upstream_character_and_relation.image_name}`,
              "image_name": upstream_character_and_relation.image_name,
              "relation": upstream_character_and_relation.relation,
              "relation_note": upstream_character_and_relation.relation_note
            });
          })

          downstream_data = {
            "name": character.value.name, "children": [], "symbolSize": 100,
            "symbol": `image://${API_BASE_URI}/images/${props.topic}/${character.value.image_name}`
          }

          response.data.downstream_characters_and_relations.forEach(function (downstream_character_and_relation, index) {
            downstream_data["children"].push({
              "name": downstream_character_and_relation.name,
              "symbolSize": 100,
              "symbol": `image://${API_BASE_URI}/images/${props.topic}/${downstream_character_and_relation.image_name}`,
              "image_name": downstream_character_and_relation.image_name,
              "relation": downstream_character_and_relation.relation,
              "relation_note": downstream_character_and_relation.relation_note
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
      handleClickCharacter,
      isUpstream,
      handleUpstreamSwitchChange,

      isRelatioinModalVisible,
      relationCharacterData,
      handleRelationModalOk
    }
  }
})
</script>

<style scoped>
.chart {
  height: 800px;
}
</style>