
<template>
  <section class="menu">
    <div v-for="(route,index) in routes" :key="index">
      <MenuItem :data="route"/>
    </div>
  </section>
</template>

<script>
import MenuItem from "./MenuItem";
export default {
  name: "Menu",
  components: {
    MenuItem
  },
  computed: {
    routes() {
      return this.$router.options.routes;
    }
  }
};
</script>

<style scoped>
.menu {
  position: relative;
  background-color: #50beda;
  width: 100%;
  height: 100%;
  left: 0;
}


.menu__aside {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 25%;
}

.menu__body {
  margin-left: 25%;
}
</style>
