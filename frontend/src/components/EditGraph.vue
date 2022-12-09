
<template>

  <a-layout class="layout">
    <a-breadcrumb style="margin: 16px 0">
      <a-breadcrumb-item>
        <router-link :to='`/topics/${topic}/edit/addcharacter`'>{{$t('message.AddCharacterWizard')}}</router-link>
      </a-breadcrumb-item>
      <a-breadcrumb-item>
        <router-link :to='`/topics/${topic}/edit/characters`'>{{$t('message.EditAllCharacters')}}</router-link>
      </a-breadcrumb-item>
      <a-breadcrumb-item>
        <router-link :to='`/topics/${topic}/edit/relations`'>{{$t('message.EditAllRelations')}}</router-link>
      </a-breadcrumb-item>
      <a-breadcrumb-item>
        <router-link :to='`/topics/${topic}/edit/groups`'>{{$t('message.EditAllGroups')}}</router-link>
      </a-breadcrumb-item>
    </a-breadcrumb>

    <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">
      <router-view></router-view>
    </div>
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
