

<template>
    
  <a-layout class="layout">

    <a-layout-header>
      <div class="logo" />
      <a-menu
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="1"><router-link to='/'>Home</router-link></a-menu-item>
        <a-menu-item key="2"><router-link :to='`/topics/${currentTopicName}/graph`'>Graph</router-link></a-menu-item>
        <a-menu-item key="3"><router-link :to='`/topics/${currentTopicName}/edit`'>Edit</router-link></a-menu-item>
        <a-menu-item key="4"><router-link :to='`/topics/${currentTopicName}/cards`'>Cards</router-link></a-menu-item>
        <a-menu-item key="5"><router-link :to='`/topics/${currentTopicName}/paths`'>Paths</router-link></a-menu-item>
        <a-menu-item key="6"><router-link to='/topics/edit'>Edit Topics</router-link></a-menu-item>
        <!-- TODO: float:right does not work-->
        <a-menu-item key="7" :disabled="true" style="float:rigt">
            <a-select
                v-model:value="currentTopicName"
                show-search
                placeholder="Select topic"
                style="width: 200px"
                :options="selectTopicOptions"
                @change="handleChangeTopic"
            >
            </a-select>
        </a-menu-item>
      </a-menu>

    </a-layout-header>

    <a-layout-content style="padding: 0 50px">
      <router-view></router-view>
    </a-layout-content>

    <a-layout-footer style="text-align: center">
      GraphBook ©2023 created by <a href="https://github.com/tobegit3hub/GraphBook">GraphBook</a>
    </a-layout-footer>
  </a-layout>

</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { SelectTypes } from 'ant-design-vue/es/select';

type SelectItem = {
  value: string;
  label: string;
};

export default defineComponent({
  name: "Home",

  setup() {
    const currentTopicName = ref("");
    const selectTopicOptions = ref<SelectTypes['options']>([]);

    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const handleChangeTopic = (value: string) => {
      // TODO: Update the child node
      //console.log(`selected ${currentTopicName.value}`);
    };

    const initTopicOptions = () => {
      axios.get(`http://127.0.0.1:7788/api/topics`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.topics.forEach(theTopic => {
            selectItems.push({"value": theTopic, "label": theTopic})
          });
          selectTopicOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      initTopicOptions();
    })

    return {
      selectTopicOptions,
      currentTopicName,
      filterOption,
      handleChangeTopic,
    };
  }

});

</script>
