<script setup>
import GraphDetail from './components/GraphDetail.vue';
import NodesTable from './components/NodesTable.vue';
import EdgesTable from './components/EdgesTable.vue';
import GroupsTable from './components/GroupsTable.vue';
import NodesCards from './components/NodesCards.vue';
import ComputeNodesPath from './components/ComputeNodesPath.vue'
</script>

<template>

    <GraphDetail db-name="cyberpunk_edgerunner"></GraphDetail>

    <!--
    <ComputeNodesPath db-name="cyberpunk_edgerunner"></ComputeNodesPath>
    -->

    <!--
    <NodesTable db-name="cyberpunk_edgerunner"></NodesTable>
    <EdgesTable db-name="pantheon"></EdgesTable>
    <GroupsTable db-name="pantheon"></GroupsTable>
    -->

    <!--
    <NodesCards db-name="cyberpunk_edgerunner"></NodesCards>
    -->
</template>
