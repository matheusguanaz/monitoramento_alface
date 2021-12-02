<template>
  <section class="parent">
  <div class="alinhar">
    <h1>Dashboard</h1>
    <router-view></router-view>
    <b-button @click="glinha()">Linha</b-button>
    <b-button @click="violino()"> Box</b-button>
    <div class="projeto-container">
    <div v-if="linha">
      <line-chart :chart-data="datacollection" width="1100%"></line-chart>
    </div>
    <div v-if="!linha">
      <violin-chart :chart-data="datacollection" width="1100%"></violin-chart>
    </div>
    </div>
    <div>
      <div class="projeto-container">
        <div>
          <b-dropdown id="dropdown-1" text="Selecione ..." width="100%">
            <b-dropdown-item id="valor2" value=2 @click="fillData('umidade_ar')">Umidade do Ar</b-dropdown-item>
            <b-dropdown-item @click="tema('luminosidade')">Luminosidade</b-dropdown-item>
            <b-dropdown-item @click="tema('temperatura')">Temperatura</b-dropdown-item>
            <b-dropdown-item @click="tema('uv')">UV</b-dropdown-item>
          </b-dropdown>
        </div>
        <div> 
          <b-form-datepicker id="example-datepicker" v-model="value"  width="100%"></b-form-datepicker>
        </div>
        <div>
          <b-form-datepicker id="example-datepicker1" v-model="value1"  width="100%"></b-form-datepicker>
        </div>
      </div>
      <div>
        <br>
        <h3>Últimas Medidas</h3>
        <br>
        <b-row>
          <b-col>Luminosidade:  {{luminosidade}}</b-col>
          <b-col>Umidade do Ar:  {{umidade_ar}}%</b-col>
          <b-col>Temperatura:  {{temperatura}}°C</b-col>
          <b-col>UV:  {{uv}}</b-col>
          <b-col v-bind:class="[tempos > 12 ? 'vermelho' : 'azul']">Água Utilizada: {{tempos.toFixed(3)}} L</b-col>
          <b-col>
            <b-button @click="encherTanque()">Encher</b-button>
          </b-col>
        </b-row>
      </div>
    </div>
  </div>
  </section>
  
</template>

<script>
 import axios from 'axios';
 import LineChart from './LineChart.js';
 import ViolinChart from './ViolinChart.js';



  export default {
    components: {
      LineChart,
      ViolinChart
    },
     data () {
      const now = new Date()
      let today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      //today = String(now.getFullYear())+ "-" + String(now.getMonth()+1) + "-" + String(now.getDate())
      let today1 = today.getFullYear().toString()+ "-" + ((today.getMonth()+1) < 9 ? "0"+String(today.getMonth()+1) : String(today.getMonth()+1))  + "-" +(today.getDate()<9 ? "0"+today.getDate().toString() : today.getDate().toString())
      //let resultado = await axios.get(process.env.VUE_APP_URL + '/datas');
      // eslint-disable-next-line
      console.log(now.getDate());
      

      return {
        datacollection: null,
        value: today1,
        value1: today1,
        luminosidade: 0,
        umidade_ar: 0,
        temperatura: 0,
        uv: 0,
        tempos: 0,
        selected: 4,
        field1: '',
        field2: '',
        field3: '',
        linha: true,
        assunto : "temperatura",
        unidadeDeMedida: ''
        //items: [{luminosidade : 30},{umidade_ar : 1.5}]
      }
    },
    async beforeMount(){
        await this.att_values_1()
    },
    async mounted () {
      await this.fillData('temperatura')
    },
    methods: {
     async fillData (value) {
       if(value=='temperatura'){
         this.unidadeDeMedida = '°C';
       }
       else if(value == 'luminosidade'){
         this.unidadeDeMedida = 'V';
       }
       else if(value == 'uv'){
         this.unidadeDeMedida = '';
       }
       else if(value == 'umidade_ar'){
         this.unidadeDeMedida = '%'
       }
       this.datacollection = null;
        this.datacollection = {
          labels: this.linha === true ? await this.getData2(value) : await this.getDataViolino2(value), // eixo X
          datasets: [
            {
              label: value == null ? 'umidade Solo' : value + " (" + this.unidadeDeMedida + ")",
              backgroundColor: 'blue',
              cubicInterpolationMode: 'monotone',
              data: this.linha === true ? await this.getData(value) : await this.getDataViolino(value), // eixo Y
            }
          ]
        }
      },
      async tema(assunto){
        this.assunto = assunto;
        await this.fillData(this.assunto);
      },
      async violino(){
        this.linha = false;
        await this.fillData(this.assunto);
      },
      async glinha(){
        this.linha = true;
        await this.fillData(this.assunto);
      },
        async getData(valor){
        let carga = {
          "inf":valor,
          "data_inicio":this.value,
          "data_fim":this.value1
        }
        let resultado = await axios.post(process.env.VUE_APP_URL + '/datas',carga);
        let resposta = [];
        for(let i=0;i<resultado.data.length;i++){
          resposta.push(resultado.data[i].valor_medio)
        }
        // eslint-disable-next-line
        console.log(resposta);
        return resposta;
      },
      async getDataViolino(valor){
        let carga = {
          "inf":valor,
          "data_inicio":this.value,
          "data_fim":this.value1
        }
        let resultado = await axios.post(process.env.VUE_APP_URL + '/violino',carga);
        let resposta = [];
        let respostas = [];
        let datas = []
        for(let i=0;i<resultado.data.length;i++){
          datas.push(resultado.data[i].data.split(' ')[0])
        }
        datas = datas.filter((v, i, a) => a.indexOf(v) === i);
        let j = 0;
        for(let i=0;i<resultado.data.length;i++){
          if(resultado.data[i].data.split(' ')[0]===datas[j]){
            resposta.push(resultado.data[i].valor_medio)
          }
          else{
            respostas.push(resposta);
            resposta = []
            j++;
            resposta.push(resultado.data[i].valor_medio)
          }
        }
        respostas.push(resposta)
        // eslint-disable-next-line
        console.log(resposta);
        return respostas;
      },
      async getDataViolino2(valor){
        let carga = {
          "inf":valor,
          "data_inicio":this.value,
          "data_fim":this.value1
        }
        let resultado = await axios.post(process.env.VUE_APP_URL + '/violino',carga);
        let resposta = [];
        for(let i=0;i<resultado.data.length;i++){
          resposta.push(resultado.data[i].data.split(' ')[0])
        }
        resposta = resposta.filter((v, i, a) => a.indexOf(v) === i);
        // eslint-disable-next-line
        console.log(resposta);
        return resposta;
      },
      async getData2(valor){
        let carga = {
          "inf":valor,
          "data_inicio":this.value,
          "data_fim": this.value1
        }
        let resultado = await axios.post(process.env.VUE_APP_URL + '/datas',carga);
        let resposta = [];
        for(let i=0;i<resultado.data.length;i++){
          resposta.push(resultado.data[i].data)
        }
        // eslint-disable-next-line
        console.log(resposta);
        return resposta;
      },
      async setModOperacao(mod_operacao){
        let carga ={
          "modo_operacao":mod_operacao,
          "periodo_rega": this.field1,
          "tempo_rega":this.field2
        };
        await axios.put(process.env.VUE_APP_URL + '/datas',carga)

      },
      async encherTanque(){
        await axios.get(process.env.VUE_APP_URL + '/encher');
      }
      ,
      async att_values_1(){
          let resultado = await axios.get(process.env.VUE_APP_URL + '/datas');
          this.temperatura = resultado.data[0].temperatura;
          this.umidade_ar = resultado.data[0].umidade_ar;
          this.luminosidade = resultado.data[0].luminosidade;
          this.uv = resultado.data[0].uv;
          resultado = await axios.get(process.env.VUE_APP_URL + '/tempos');
          this.tempos = parseFloat(resultado.data[0].tempos);
          for(let i = 1; i<3;i++){
            let resultado_alerta = await axios.post(process.env.VUE_APP_URL + '/dispositivo',{"id_planta":String(i)});
            try {
              if(resultado_alerta.data[0].umidade_atual != "" && Number(resultado_alerta.data[0].umidade_atual) < 30 && Number(resultado_alerta.data[0].tempo_plantado) > 7200){
                alert("Dispositivo de id "+i.toString()+"está com algum defeito");
              }
            } catch (error) {
              // eslint-disable-next-line
              console.log(error);
            }
            
          }
          setTimeout(this.att_values_1, 2000);
      }
    }
  }
</script>

<style>
.projeto-container{
    display: flex;
}
.projeto-container1{
  display: flex;
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 88%;
  height: 60%;
}
.grafico{
  width: 800px;
}
.classe-button{
  color: blue;
}

.azul{
  color: black;
}

.vermelho{
  color: red;
}

</style>
