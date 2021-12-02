<template>
  <div id="app">
    <div class="inline-block">
      <router-view></router-view>
      <div> 
    <b-button v-b-toggle.sidebar-1>Menu</b-button>
    <b-sidebar id="sidebar-1" bg-variant="info" class="azul1">
      <div class="px-3 py-2 azul">
        <b-link class="classe-link" href="/#/parent-1" v-b-toggle.sidebar-1>  Dashboard<br><br></b-link>
        <b-link class="classe-link" href="/#/parent-2" v-b-toggle.sidebar-1>  Dispositivos<br><br></b-link>
        <b-link class="classe-link" href="/#/operacao" v-b-toggle.sidebar-1>  Modos de Operação<br> do Sistema<br></b-link>
      </div>
    </b-sidebar>
  </div>
    </div>
  </div>
</template>

<script>
require('dotenv').config();
export default {
  name: "App",

};
</script>

<style>
html,
body {
  height: 100%;
  width: 100%;
}
.inline-block {
  display: inline-flex;
  height: 56%;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
  width: 100%;
  margin-top: 0px;
}
.parent {
  color:black;
}
.child {
  color: #96A8B4;
}

.sub-child {
  color: #AEC5A9;
}
</style>
