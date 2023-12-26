
<template>

  <div style="background-color: #ececec; padding: 20px">

    <!-- Form to choose characteer -->
    <h1>{{$t('ChooseCharacter')}}</h1>
    <a-select v-model:value="currentSelectedCharacter" show-search :placeholder="$t('Character')" style="width: 200px"
      :options="selectCharacterOptions" :filter-option="filterOption" @change="changeSelectedCharacter"></a-select>

    <br /><br />
    <!-- Only show when not selecting character -->
    <div v-if="!currentSelectedCharacter">
      <h1>{{$t('CharacterList')}}</h1>
      <a-row :gutter="16">
        <div v-for="character in characters" @click="chooseCharacterFromImage(character.name)">
          <a-col :span="4">
            <a-card hoverable style="width: 240px">
              <!-- 240px by default-->
              <template #cover>
                
              </template>
              <a-card-meta :title="character.name">
                <template #description>{{ character.note }}</template>
              </a-card-meta>
            </a-card>
          </a-col>
        </div>
      </a-row>
    </div>

    <!-- Character detail -->
    <div>
      <router-view></router-view>
    </div>

  </div>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted, watch } from 'vue'
import type { SelectProps } from 'ant-design-vue';
import { useRoute, useRouter } from 'vue-router'

type SelectItem = {
  value: string;
  label: string;
};


export default defineComponent({
  name: "ChooseCharacters",
  props: {
    topic: String,
  },
  setup(props) {
    const API_BASE_URI = axios.defaults.baseURL;

    const route = useRoute()
    const router = useRouter()

    const characters = ref([]);

    const currentSelectedCharacter = ref<string>();
    const selectCharacterOptions = ref<SelectProps['options']>([]);

    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const changeSelectedCharacter = () => {
      // Go to the character detail page
      router.push({ path: `/topics/${props.topic}/characters/${currentSelectedCharacter.value}` })
    }

    const chooseCharacterFromImage = (character_name) => {
      currentSelectedCharacter.value = character_name;
      changeSelectedCharacter();
    }

    watch(() => props.topic, (first, second) => {
      init();
    });

    const init = () => {

      if (route.params.character_name) {
        // Get route to set selecter default value
        currentSelectedCharacter.value = route.params.character_name;
      }

      axios.get(`/api/topics/${props.topic}/characters`)
        .then(response => {
          characters.value = response.data.characters;

          const selectItems: SelectItem[] = [];
          response.data.characters.forEach(character => {
            selectItems.push({ "value": character.name, "label": character.name })
          });
          selectCharacterOptions.value = [...selectItems];

        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      init()
    })

    return {
      API_BASE_URI,

      characters,

      currentSelectedCharacter,
      filterOption,
      selectCharacterOptions,
      changeSelectedCharacter,

      chooseCharacterFromImage
    }
  }
})
</script>
