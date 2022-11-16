
<template>

<div style="background-color: #ececec; padding: 20px">
    <a-row :gutter="16">


      <div v-for="character in characters">
     
        <a-col :span="4">
          <a-card hoverable style="width: 240px">
          <template #cover>
            <img :src="'http://localhost:7788/images/' + topic + '/' + character.name + '.png'" />
          </template>
          <a-card-meta :title="character.name">
            <template #description>{{ character.note }}</template>
          </a-card-meta>
        </a-card>
        </a-col>

      </div>


    </a-row>
  </div>


</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'
import { VXETable, VxeGridInstance, VxeGridListeners, VxeGridProps } from 'vxe-table'

export default defineComponent({
  name: "CharactersCard",
  props: {
    topic: String,
  },
  setup (props) {
   
    let characters = ref([]);

    onMounted(() => {
      axios.get(`http://127.0.0.1:7788/api/topics/${props.topic}/characters`)
        .then(response => {
          characters.value = response.data.characters;
        })
        .catch(error => {
          console.log(error);
        });
    })

    return {
      characters
    }
  }
})
</script>
