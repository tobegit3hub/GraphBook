
<template>

  <br />
  <!-- Echarts Graph -->
  <v-chart class="chart" :option="vuechartOption" @dblclick="doubleClickGraph" />

  <!-- The modal to show single event -->
  <a-modal v-model:visible="isModalVisible" :title="modalTitle" @ok="handleModalOk">
    <br/>
    <p>{{ modalNote }}</p>

    <br/>
    <h3>{{ $t('message.RelatedCharacters') }}</h3>
    <a-list :grid="{ gutter: 16, column: 4 }" :data-source="modalRelatedCharacters">
      <template #renderItem="{ item }">
        <a-list-item>
          <a-card hoverable @click="redirectToCharacterPage(item.name)">
              <template #cover>
                  <img v-if="item.image_name" :src="`${API_BASE_URI}/images/${topic}/${item.image_name}`" />
              </template>
              <a-card-meta :title="item.name">
                <template #description>{{ item.note }}</template>
              </a-card-meta>
            </a-card>
        </a-list-item>
      </template>
    </a-list>

  </a-modal>

</template>

<script>
import { defineComponent, ref, reactive, watch, toRefs, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import VChart from "vue-echarts";

export default defineComponent({
  name: "MainlineDetail",
  props: {
    topic: String
  },
  components: {
    VChart
  },
  setup(props) {
    const API_BASE_URI = axios.defaults.baseURL;

    const router = useRouter();

    const simplifyNote = (note) => {
      if (note) {
        if (note.length > 6) {
          return note.substring(0, 10) + "...";
        } else {
          return note;
        }
      } else {
        return null;
      }
    };

    const vuechartOption = ref({
      backgroundColor: '#f6f5f3',
      title: {
        text: props.topic,
        textStyle: {
          fontWeight: 700,
          fontSize: 30,
          left: 'center'
        }
      },
      legend: {
        show: true
      },
      tooltip: {
        trigger: "item",
        formatter: (param) => {
          let template = param.data.name;
          if (param.data.name) {
            if (param.data.note) {
              template += '<br/><br/>'
              template += '<div style="width: 100px">' + simplifyNote(param.data.note) + '</div>';
            }
          }
          return template;
        }
      },
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
          label: {
            show: true,
            fontStyle: 'normal',
            fontSize: 15,
          },
          symbolSize: 80,
          itemStyle: {
            shadowColor: '#C0C0C0',
            shadowOffsetX: 2,
            shadowOffsetY: 2,
          },
          roam: true,
          draggable: true,
          edgeSymbol: ['circle', 'arrow'],
          edgeSymbolSize: [5, 10],
          edgeLabel: {
            show: false,
            fontSize: 12,
            color: '#000000'
          },
          cursor: 'pointer',
          emphasis: {
            scale: true,
            // TODO: Not the chain of this element, refer to https://echarts.apache.org/en/option.html#series-graph
            focus: 'series'
          },
          lineStyle: {
            color: '#3d3d3f',
            width: 2,
            curveness: 0
          },
          data: [],
          links: []
        }]
    })

    watch(() => props.topic, (first, second) => {
      init();
      // Manually update the title of the graph
      vuechartOption.value.title.text = props.topic;
    });

    onMounted(() => {
      init();
    })

    const init = () => {
      axios.get(`/api/topics/${props.topic}/mainlines/graph_data`).then(response => {

        vuechartOption.value.series[0].categories = response.data.categories;

        const series_0 = vuechartOption.value.series[0];
        series_0.data = response.data.nodes;
        vuechartOption.value.series[0] = series_0;

        vuechartOption.value.series[0].links.push(...response.data.edges);

      }, response => {
        console.log(`Fail to get characters for topic: ${props.topic}`);
      });
    }


    const redirectToCharacterPage = (character_name) => {
      router.push({ path: `/topics/${props.topic}/characters/${character_name}` })
    }

    const isModalVisible = ref(false);
    const modalTitle = ref("");
    const modalNote = ref("");
    const modalRelatedCharacters = ref([]);

    const handleModalOk = (e) => {
      isModalVisible.value = false;
    };

    const doubleClickGraph = (params) => {
      isModalVisible.value = true;
      modalTitle.value = params.data.name;
      modalNote.value = params.data.note;

      // Get related characters
      modalRelatedCharacters.value.splice(0);
      axios.post(`/api/topics/${props.topic}/related_characters`, {
        text: params.data.note
      }).then(response => {
        modalRelatedCharacters.value.push(...response.data.characters);
      }, response => {
        console.log(`Fail to get related characters for topic: ${props.topic}`);
      });
    }


    return {
      API_BASE_URI,

      init,
      vuechartOption,
      doubleClickGraph,

      isModalVisible,
      handleModalOk,
      modalTitle,
      modalNote,
      modalRelatedCharacters,
      redirectToCharacterPage
    }

  }
})

</script>

<style scoped>
.chart {
  height: 800px;
}
</style>