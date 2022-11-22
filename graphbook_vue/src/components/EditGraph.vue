
<template>




  <a-layout>
      <a-layout-sider width="200" style="background: #fff">
        <a-menu
          mode="inline"
          :style="{ height: '100%', borderRight: 0 }"
        >
          <a-menu-item key="1"><router-link :to='`/topics/${topic}/edit/characters`'>Edit characters</router-link></a-menu-item>
          <a-menu-item key="2"><router-link :to='`/topics/${topic}/edit/relations`'>Edit relations</router-link></a-menu-item>
          <a-menu-item key="3"><router-link :to='`/topics/${topic}/edit/groups`'>Edit groups</router-link></a-menu-item>
        </a-menu>
      </a-layout-sider>

      <a-layout style="padding: 0 24px 24px">
        <a-layout-content
          :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
        >
          
          <router-view></router-view>

        </a-layout-content>
      </a-layout>
    </a-layout>





</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: "EditGraph",
  props: {
    topic: String,
  },
  setup() {
  }
})
</script>
