
<template>

  <div style="background-color: #ececec; padding: 20px">

    <h1>{{$t('message.Group')}}: {{ group }}</h1>

    <br/>
    <div v-for="character in groupCharactersData">
      <a-card hoverable @click="redirectToCharacterPage(character.name)">
        <template #cover>
            <img v-if="character.image_name" :src="`${API_BASE_URI}/images/${topic}/${character.image_name}`" />
        </template>
        <a-card-meta :title="character.name">
          <template #description>{{ character.note }}</template>
        </a-card-meta>
      </a-card>
    </div>

  </div>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

interface CharacterData {
  name: string,
  weight: string,
  note: string,
  image_name: string
}

export default defineComponent({
  name: "GroupDetail",
  props: {
    topic: String,
    group: String,
  },
  setup(props) {
    const API_BASE_URI = axios.defaults.baseURL;

    const router = useRouter()

    const groupCharactersData = ref<CharacterData[]>();

    const redirectToCharacterPage = (character_name) => {
      router.push({ path: `/topics/${props.topic}/characters/${character_name}` })
    }

    watch(() => props.topic, (first, second) => {
      init();
    });

    const init = () => {
        axios.get(`/api/topics/${props.topic}/groups/${props.group}/characters`)
        .then(response => {
          groupCharactersData.value = response.data.characters;
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

      groupCharactersData,

      redirectToCharacterPage
    }
  }
})
</script>
