
<template>

<div style="background-color: #ececec; padding: 20px">

  <h1>Character cards</h1>
  <a-row :gutter="16">
    <div v-for="character in characters">
      <a-col :span="4">
        <a-card hoverable style="width: 80px"> <!-- 240px by default-->
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

  <!-- Character detail -->
  <div>
    <router-view></router-view>
  </div>

</div>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted} from 'vue'
import type { SelectProps } from 'ant-design-vue';
import { useRouter, useRoute } from 'vue-router'

type SelectItem = {
  value: string;
  label: string;
};

export default defineComponent({
  name: "CharactersCards",
  props: {
    topic: String,
  },
  setup (props) {
    const router = useRouter()

    const characters = ref([]);

    onMounted(() => {
      axios.get(`/api/topics/${props.topic}/characters`)
        .then(response => {
          characters.value = response.data.characters;

          const selectItems: SelectItem[] = [];
          response.data.characters.forEach(character => {
            selectItems.push({"value": character.name, "label": character.name})
          });
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
