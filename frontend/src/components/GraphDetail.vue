<template>

<!-- The modal to show character -->
<a-modal v-model:visible="isShowCharacterModal" title="Character Detail" @ok="handleCharacterModalOk">
  <p>{{ $t('Name') }}: 
    <router-link :to='`/topics/${topic}/characters/${currentCharacter.name}`'>{{
      currentCharacter.name
    }}</router-link>
  </p>

  <p>{{ $t('Alias') }}: {{ currentCharacter.alias }}</p>

  <p>{{ $t('Weight') }}: {{ currentCharacter.weight }}</p>

  <p>{{ $t('Note') }}:</p>
  <p>{{ currentCharacter.note }}</p>
</a-modal>

<!-- The modal to show relation -->
<a-modal v-model:visible="isShowRelationModal" title="Relation Detail" @ok="handleRelationModalOk">
  <a-row justify="space-around" align="middle">
    <a-col :span="4">
      <p>{{ $t('Name') }}: 
      <router-link :to='`/topics/${topic}/characters/${currentCharacter.name}`'>{{
        currentCharacter.name
      }}</router-link>
    </p>

    <p>{{ $t('Weight') }}: {{ currentCharacter.weight }}</p>

    <p>{{ $t('Note') }}:</p>
    <p>{{ currentCharacter.note }}</p>
    </a-col>
    <a-col :span="4">
      <p class="height-50">Sample relation</p>
    </a-col>
    <a-col :span="4">
      <p>{{ $t('Name') }}: 
      <router-link :to='`/topics/${topic}/characters/${currentTargetCharacter.name}`'>{{
        currentTargetCharacter.name
      }}</router-link>
    </p>

    <p>{{ $t('Weight') }}: {{ currentTargetCharacter.weight }}</p>

    <p>{{ $t('Note') }}:</p>
    <p>{{ currentTargetCharacter.note }}</p>
    </a-col>
  </a-row>
</a-modal>

<div v-if="!onlyGraph">
  <!-- Choose the character -->
  <br/>
  <a-form
    :model="chooseCharacterForm">
    <a-form-item
      :label="$t('Choose character')">
      <a-select show-search v-model:value="chooseCharacterForm.name" @select="handleChooseCharacter">
        <option v-for="character in allCharacters" :value="character.name + ' (' + character.alias + ')'">{{ character.name }}</option>
      </a-select>
    </a-form-item>
  </a-form>
</div>

<v-chart class="chart" :option="chartOption" @click="handleClickGraph" />

<div v-if="!onlyGraph">
  <h1>hello</h1>
  <h1>{{ topic }}</h1>
</div>

</template>

<script>
import axios from 'axios';
import VChart from "vue-echarts";

export default {
  components: {
    VChart
  },

  props: {
    topic: String,
    onlyGraph: Boolean
  },

  data() {
    return {
      // Graph data
      allCharacters: [],
      allGroupNames: [],

      // Modal
      isShowConfigModal: false,
      isShowCharacterModal: false,
      isShowRelationModal: false,
      currentCharacter: null,
      currentTargetCharacter: null,
      currentRelation: "",

      // Graph config
      graphConfig: {
        isUseNodeWeight: true,

      },
      symbolSize: 80,
      labelFontSize: 15,


      // Form
      chooseCharacterForm: {
        name: '',
      },

      // Chart config
      chartOption: {
        title: {
          text: this.topic,
          left: 'center',
          textStyle: {
            fontSize: 20,
            left: 'center'
          }
        },
        legend: {
          show: true
        },
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            type: 'graph',
            layout: 'force',
            force: {
              repulsion: [1000, 1200],
              layoutAnimation: true,
              friction: 0.3,
              edgeLength: [100, 130]
            },
            symbolSize: 50,
            roam: true,
            draggable: true,
            focusNodeAdjacency: true,
            label: {
              show: true
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
              fontSize: 20
            },
            itemStyle: {
              shadowColor: '#C0C0C0',
            },
            emphasis: {
              scale: true,
              focus: 'adjacency'
            },
            lineStyle: {
              opacity: 0.9,
              width: 2,
              curveness: 0
            },
            data: [],
            links: [],
          }
        ]
      },



    };
  },

  mounted() {
    this.init();
  },

  methods: {
    init() {
      // Get all the characters
      axios.get(`/api/topics/${this.topic}/characters`).then(response => {
        this.allCharacters = response.data.characters;

        this.updateGraphCharacters(this.allCharacters);
      });

      // Get all the relations
      axios.get(`/api/topics/${this.topic}/relations`).then(response => {
        this.chartOption.series[0].links = response.data.relations;
      });

      // Get all the groups
      axios.get(`/api/topics/${this.topic}/groups_names`).then(response => {
        this.allGroupNames = response.data.groups_names;
      });
  
    },

    // Update the graph
    updateGraphCharacters(charactersInfos) {
      const isUseNodeWeight = this.graphConfig.isUseNodeWeight;
      
      charactersInfos.forEach(function (characterInfo, index, array) {
        if (isUseNodeWeight) {
          charactersInfos[index]["symbolSize"] = characterInfo.weight * 500;
        }
      });
        
      this.chartOption.series[0].data = charactersInfos;
    },

    handleChooseCharacter() {

      console.log(this.chooseCharacterForm.name);

    },

    handleCharacterModalOk() {
      this.isShowCharacterModal = false;
    },

    handleRelationModalOk() {
      this.isShowRelationModal = false;
    },

    // Click the graph
    handleClickGraph(params) {
      
      if (params.data.name) { // Click the node
        

        const characterName = params.data.name;
        axios.get(`/api/topics/${this.topic}/characters/${characterName}`).then(response => {
          this.currentCharacter = response.data.character;

          this.isShowCharacterModal = true;
        });
      } else if (params.data.source && params.data.target) { // Click the edge
        

        const sourceCharacterName = params.data.source;
        const targetCharacterName = params.data.target;

        axios.get(`/api/topics/${this.topic}/characters/${sourceCharacterName}`).then(response => {
          this.currentCharacter = response.data.character;  
        });

        axios.get(`/api/topics/${this.topic}/characters/${targetCharacterName}`).then(response => {
          this.currentTargetCharacter = response.data.character;

          this.isShowRelationModal = true;
        });

        /*
        axios.get(`/api/topics/${this.topic}/relations/${sourceName}/${targetName}`).then(response => {
          this.currentRelation = response.data.relation;

          this.isShowEdgeModal = true;
        });
        */
      }

      /*
      const characterName = params.data.name;
      axios.get(`/api/topics/${this.topic}/characters/${characterName}`).then(response => {
        this.currentCharacter = response.data.character;

        this.isShowCharacterModal = true;
      });
      */

    },

  },

  watch: {
    // Convert all watch() from setup() here
    'props.topic': function(newVal, oldVal) {
      // watch logic
    },
    // ... other watchers
  },

};
</script>

<style scoped>
.chart {
 height: 800px;
}
</style>