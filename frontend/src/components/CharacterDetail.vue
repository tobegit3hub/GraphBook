
<template>

  <div v-if="character">

    <!-- Modal to show relation -->
    <a-modal v-model:visible="isRelatioinModalVisible" title="Relation" width="1000px" @ok="cancelModel">
      <a-row>
        <a-col :span="8">
          <h3><router-link :to='`/topics/${topic}/characters/${character.name}`'>{{ character.name }}</router-link></h3>
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
          <h3><router-link :to='`/topics/${topic}/characters/${relationCharacterData.name}`' @click="cancelModel">{{
              relationCharacterData.name
          }}</router-link></h3>
        </a-col>
      </a-row>

    </a-modal>

    <br />
    <!-- Detail of character -->
    <h1>{{ character.name }}</h1>
    <p>{{ $t('Name') }}: {{ character.name }}</p>
    <p>{{ $t('Weight') }}: {{ character.weight }}</p>
    <p>{{ $t('Note') }}: {{ character.note }}</p>
  </div>

  <br/>
  <h2>{{$t('Groups')}}</h2>
  <a-list :data-source="characterGroups">
      <template #renderItem="{ item }">
        <a-list-item>
          <router-link :to='`/topics/${topic}/groups/${item}`'>{{ item }}</router-link>
        </a-list-item>
      </template>
    </a-list>

  <br /><br />
  <!-- The graph of all associated characters -->
  <h2>{{ $t('AssociatedCharacters') }}</h2>
  <a-switch v-model:checked="isUpstream" :checked-children="$t('Upstream')"
    :un-checked-children="$t('Downstream')" @change="handleUpstreamSwitchChange" />
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
          animationDuration: 550,
          animationDurationUpdate: 750
        }]
    })

    const characterGroups = ref([]);

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

    const cancelModel = () => {
      isRelatioinModalVisible.value = false;
    };

    const handleClickCharacter = (params) => {

      if (params.data.name != character.value.name) {
        isRelatioinModalVisible.value = true;
        relationCharacterData.value = {
          "name": params.data.name,
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
      characterGroups.value.splice(0);
      axios.get(`/api/topics/${props.topic}/characters/${props.character_name}/groups`).then(response => {
        characterGroups.value.push(...response.data.groups)
      }, response => {
        console.log(`Fail to get character groups for character: ${props.character_name}`);
      });

      axios.get(`/api/topics/${props.topic}/characters/${props.character_name}/relations`)
        .then(response => {
          character.value = response.data.character;

          upstream_data = {
            "name": character.value.name, "children": [], "symbolSize": 100
          }

          response.data.upstream_characters_and_relations.forEach(function (upstream_character_and_relation, index) {
            const children_item = {
              "name": upstream_character_and_relation.name,
              "symbolSize": 100,
              "relation": upstream_character_and_relation.relation,
              "relation_note": upstream_character_and_relation.relation_note
            }
            upstream_data["children"].push(children_item);
          })

          downstream_data = {
            "name": character.value.name, "children": [], "symbolSize": 100
          }

          response.data.downstream_characters_and_relations.forEach(function (downstream_character_and_relation, index) {
            const children_item = {
              "name": downstream_character_and_relation.name,
              "symbolSize": 100,
              "relation": downstream_character_and_relation.relation,
              "relation_note": downstream_character_and_relation.relation_note
            };
            downstream_data["children"].push(children_item);
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
      characterGroups,

      vuechartOption,
      handleClickCharacter,
      isUpstream,
      handleUpstreamSwitchChange,

      isRelatioinModalVisible,
      relationCharacterData,
      cancelModel
    }
  }
})
</script>

<style scoped>
.chart {
  height: 800px;
}
</style>