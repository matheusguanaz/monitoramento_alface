//libs
import Vue from "vue";
import Router from "vue-router";

//Components
//-----Parent 1
import Parent1 from "./components/Parent1/";
//import Parent1Child1 from "./components/Parent1/Child1";
//import Parent1Child2 from "./components/Parent1/Child2";
//import Parent1SubChild1 from "./components/Parent1/SubChild1";
//import Parent1SubChild2 from "./components/Parent1/SubChild2";
//-----Parent 2
import Parent2 from "./components/Parent2/";
//import Parent2Child1 from "./components/Parent2/Child1";
//-----Parent 3
import Parent3 from "./components/Parent3/";
import Dispositivos from "./components/dispositivo.vue";
import ModoOperacao from "./components/modo_operacao.vue";
//-----Not Found
import NotFound from "./components/NotFound";
Vue.use(Router);

export default new Router({
  routes: [
    //default route redirection
    { path: "/", redirect: { name: "Parent1" } },
    //not found route redirection
    { path: "*", component: NotFound },
    {
      path: "/parent-1",
      name: "Parent1",
      component: Parent1,
      meta: {
        label: "Dashboard"
      },

    },
    {
      path: "/parent-2",
      name: "Parent2",
      component: Parent2,
      meta: {
        label: "Dispositivos"
      }
    },
    {
      path:"/dispositivo",
      name: "Dispositivo",
      component: Dispositivos
    },
    {
      path:"/operacao",
      name: "Modo Operação",
      component: ModoOperacao,
      meta: {
        label : "Modo de Operação"
      }
    },
    {
      path: "/parent-3",
      name: "Parent3",
      component: Parent3
    },
    {
      path: "/not-found",
      name: "not Found",
      component: NotFound,
      meta: {
        display: false // this attribute i use it to show/hide route in th menu
      }
    }
  ]
});
