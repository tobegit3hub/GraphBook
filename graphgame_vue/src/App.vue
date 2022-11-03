<script setup>
import GraphDetail from './components/GraphDetail.vue';
import NodesTable from './components/NodesTable.vue';
import EdgesTable from './components/EdgesTable.vue';
</script>

<template>
    <!-- <GraphDetail></GraphDetail> -->
    <NodesTable db-name="cyberpunk_edgerunner"></NodesTable>
    <EdgesTable db-name="cyberpunk_edgerunner"></EdgesTable>

</template>
