<template>
  <section class="parent">

    <div class="alinhar">
    <h1>Dispositivos</h1>
    <b-table striped hover :items="dispositivos" :fields="fields">
        <template slot="cell(visualizar)" slot-scope="{ item: { id_planta }}">
            <b-button v-on:click="redirect(id_planta)">
              Visualizar
            </b-button>
            <b-button v-on:click="realizarColheita(id_planta)">
              Colheita
            </b-button>
            <b-button v-on:click="iniciarPlantacao(id_planta)">
              Iniciar
            </b-button>
        </template>
    </b-table>
    </div>
  </section>
</template>

<script>
import axios from 'axios';


export default {
  data: ()=>{
    return{
      dispositivos: [],
      fields: [
          {
              key: 'id_planta',
              label: 'ID'
          },
          {
              key: 'visualizar',
              label: ''
          },
          {
              key: 'pausar',
              label: ''
          },
          {
              key: 'iniciar',
              label: ''
          }
        ]
      }
  },
  async beforeMount(){
    await this.getValues()
  },
  methods: {
    redirect(id){
      this.$router.push(`dispositivo?${id}`);
    },
    async realizarColheita(id){
      let carga = {
        "id_planta" : id,
        "modo_operacao" : 2
      };
      await axios.put(process.env.VUE_APP_URL + '/dispositivos',carga);
    } ,
    async iniciarPlantacao(id){
      let carga = {
        "id_planta" : id,
        "modo_operacao" : 0
      };
      await axios.put(process.env.VUE_APP_URL + '/dispositivos',carga);
    },
    async getValues(){
      let resultado = await axios.get(process.env.VUE_APP_URL + '/dispositivos');
      let retorno = [];
      for(let i=0; i<resultado.data.lenght;i++){
        retorno.push(resultado.data[i].id_planta)
      }
      this.dispositivos = resultado.data;
    }
  }
};
</script>

<style>
.alinhar{
    margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
