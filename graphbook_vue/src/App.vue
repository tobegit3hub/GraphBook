<script setup>

</script>

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
        <a-menu-item key="2">Graph</a-menu-item>
        <a-menu-item key="3">Edit</a-menu-item>
        <a-menu-item key="4">Cards</a-menu-item>
        <a-menu-item key="5">Paths</a-menu-item>
      </a-menu>

      
    </a-layout-header>

    <a-layout-content style="padding: 0 50px">
      <router-view></router-view>
    </a-layout-content>

    <a-layout-footer style="text-align: center">
      GraphBook ©2023 Created at <a href="https://github.com/tobegit3hub/GraphBook">GraphBook</a>
    </a-layout-footer>
  </a-layout>


</template>
