<template>
  <section>
  <div class="alinhar">
    <h1>Dispositivo {{id_planta}}</h1>
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
    <div class="projeto-container">
      <div>
        <b-dropdown id="dropdown-1" text="Selecione ..." class="m-md-2">
          <b-dropdown-item @click="tema('umidade_atual')">Umidade do Solo</b-dropdown-item>
          <b-dropdown-item @click="tema('quantidade_agua')">Quantidade de Água</b-dropdown-item>
        </b-dropdown>
      </div>
      <div>
        <b-form-datepicker id="example-datepicker" v-model="value" class="mb-2"></b-form-datepicker>
      </div>
      <div>
        <b-form-datepicker id="example-datepicker1" v-model="value1" class="mb-2"></b-form-datepicker>
      </div>
    </div>
    <div>
      <h3>Últimas Medidas</h3>
      <br>
      <b-row>
        <b-col>Tempo Plantado <br> {{tempo_plantado}}</b-col>
        <b-col>Umidade do Solo<br> {{umidade_atual}} %</b-col>
        <b-col>Água utilizada na última rega <br> {{quantidade_agua}} L</b-col>
        <b-button v-b-modal.modoOperacao>Modo de Operação <br> do Dispositivo</b-button>
        <b-modal id="modoOperacao"
        title="Modo de Operação do Dispositivo"
        ok-title="Salvar"
        cancel-title="Cancelar"
        @ok="setModOperacao"
        >
        <b-form-group>
      <b-form-radio v-model="selected" name="some-radios" value=2>Pausado</b-form-radio>
      <b-form-radio v-model="selected" name="some-radios" value=1>Automático</b-form-radio>
      <b-form-radio v-model="selected" name="some-radios" value=0>Manual</b-form-radio>
      <div v-if="selected==0">
       <b-col sm="7">
        <div class="projeto-container">
          Periodo Rega
        <b-form-input v-model="field1" placeholder="">Periodo</b-form-input>
          <b-dropdown id="dropdown-3" :text="this.nome" class="m-md-2">
            <b-dropdown-item @click="consPeriodo(1)" >Seg</b-dropdown-item>
            <b-dropdown-item @click="consPeriodo(60)">Min</b-dropdown-item>
            <b-dropdown-item @click="consPeriodo(3600)">Hor</b-dropdown-item>
            <b-dropdown-item @click="consPeriodo(86400)">Dias</b-dropdown-item>
          </b-dropdown>
        </div>
        </b-col>
       <br>
        <b-col sm="7">
          
        <div class="projeto-container">
          Rega
        <b-form-input v-model="field2" placeholder="">Rega</b-form-input>
          <b-dropdown id="dropdown-3" :text="this.nome1" class="m-md-2">
            <b-dropdown-item @click="consTempo(1)">Seg</b-dropdown-item>
            <b-dropdown-item @click="consTempo(60)">Min</b-dropdown-item>
            <b-dropdown-item @click="consTempo(3600)">Hor</b-dropdown-item>
            <b-dropdown-item @click="consTempo(86400)">Dias</b-dropdown-item>
            <b-dropdown-item @click="consTempo(2)">mL</b-dropdown-item>
          </b-dropdown>
        </div>
        </b-col>
      </div>
      </b-form-group>
        
    </b-modal>
      </b-row>
      
    </div>
  </div>
  </section>
  
</template>

<script>
 import LineChart from './Parent1/LineChart.js'
 import ViolinChart from './Parent1/ViolinChart.js'
 import axios from 'axios';

  export default {
    components: {
      LineChart,
      ViolinChart
    },
     data () {
      const now = new Date()
      let today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      let today1 = today.getFullYear().toString()+ "-" + ((today.getMonth()+1) < 9 ? "0"+String(today.getMonth()+1) : String(today.getMonth()+1))  + "-" +(today.getDate()<9 ? "0"+today.getDate().toString() : today.getDate().toString())
      //let today1 = '2021-01-01';
      //let resultado = await axios.get(process.env.VUE_APP_URL + '/datas');
      // eslint-disable-next-line
      //console.log(today1);
      //console.log(today.getMonth()-1);
      

      return {
        datacollection: null,
        value: today1,
        value1: today1,
        id_planta:  window.location.href.split('?')[1],
        umidade_atual: 0,
        quantidade_agua: 0,
        tempo_plantado: '',
        linha: true,
        field1: '',
        field2: '',
        vlrTempo : null,
        vlrPeriodo: null,
        periodo: 1,
        tempoCons: 1,
        selected: 4,
        nome: 'Seg',
        nome1: 'Seg',
        assunto : "umidade_atual",
        qtd_agua: -1,
        unidadeDeMedida : "%"
      }
    },
    async beforeMount(){
        await this.att_values()
    },
    async mounted () {
      await this.fillData('umidade_atual'),
      this.printData(),
      this.luminosidade = 1,
       await this.defModoOper()
    },
    methods: {
      async defModoOper(){
        let resposta = await axios.get(process.env.VUE_APP_URL + '/dispositivos');
        for(let i = 0; i<resposta.data.length; i++){
          if(resposta.data[i].id_planta == this.id_planta){
            this.selected =  resposta.data[i].modo_operacao;
            if(resposta.data[i].modo_operacao==0){
              if(resposta.data[i].periodo_rega/86400 >= 1){
                this.field1 = resposta.data[i].periodo_rega/86400;
                this.nome = 'Dias'
              }
              else if(resposta.data[i].periodo_rega/3600 >= 1){
                this.field1 = resposta.data[i].periodo_rega/3600;
                this.nome = 'Hor'
              }
              else if(resposta.data[i].periodo_rega/60 >= 1){
                this.field1 = resposta.data[i].periodo_rega/60;
                this.nome = 'Min'
              }
              else{
                 this.field1 = resposta.data[i].periodo_rega;
                 this.nome = 'Seg'
              }
              if(resposta.data[i].qtd_agua==-1){
                if(resposta.data[i].tempo_rega/86400 >= 1){
                  this.field2 = resposta.data[i].tempo_rega/86400;
                  this.nome1 = 'Dias'
                }
                else if(resposta.data[i].tempo_rega/3600 >= 1){
                  this.field2 = resposta.data[i].tempo_rega/3600;
                  this.nome1 = 'Hor'
                }
                else if(resposta.data[i].tempo_rega/60 >= 1){
                  this.field2 = resposta.data[i].tempo_rega/60;
                  this.nome1 = 'Min'
                }
                else{
                  this.field2 = resposta.data[i].tempo_rega;
                  this.nome1 = 'Seg'
                }
              }
            }
          }
        }
      },
      consPeriodo(constante){
        this.vlrPeriodo = this.field1*constante;
        if(constante === 1){
          this.nome = 'Seg';
        }
        else if(constante == 60){
          this.nome = 'Min';
        }
        else if(constante == 3600){
          this.nome = 'Hor'
        }
        else if(constante == 86400){
          this.nome = 'Dias';
        }
      },
      consTempo(constante){
        this.vlrTempo = this.field2*constante;
        if(constante === 1){
          this.nome1 = 'Seg';
          this.qtd_agua = -1;
        }
        else if(constante == 60){
          this.nome1 = 'Min';
          this.qtd_agua = -1;
        }
        else if(constante == 3600){
          this.nome1 = 'Hor';
          this.qtd_agua = -1;
        }
        else if(constante == 86400){
          this.nome1 = 'Dias';
          this.qtd_agua = -1;
        }
        else if(constante == 2){
          this.nome1 = 'mL';
          this.qtd_agua = this.field2;
        }
      },
      async setModOperacao(){
        let carga ={
          "id_planta" : this.id_planta,
          "modo_operacao":this.selected,
          "periodo_rega": (this.vlrPeriodo === null ? this.field1 : this.vlrPeriodo),
          "tempo_rega":(this.vlrTempo === null ? this.field2 : this.vlrTempo),
          "qtd_agua" : this.qtd_agua
        };
        await axios.put(process.env.VUE_APP_URL + '/dispositivo',carga)
      },
     async fillData (value) {
       if(value=='umidade_atual'){
         this.unidadeDeMedida = '%';
       }
       else if(value == 'quantidade_agua'){
         this.unidadeDeMedida = 'L';
       }
       this.datacollection = null;
        this.datacollection = {
          labels: this.linha === true ? await this.getData2(value) : await this.getDataViolino2(value), // eixo X
          datasets: [
            {
              label: value == null ? 'umidade Solo' : value + " (" + this.unidadeDeMedida + ")",
              backgroundColor: 'blue',
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
          "id_planta": this.id_planta,
          "data_inicio":this.value,
          "data_fim":this.value1
        }
        let resultado = await axios.post(process.env.VUE_APP_URL + '/dispositivos',carga);
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
          "id_planta" : String(this.id_planta),
          "data_inicio":this.value,
          "data_fim":this.value1
        }
        let resultado = await axios.post(process.env.VUE_APP_URL + '/violino_disp',carga);
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
          "id_planta" : String(this.id_planta),
          "data_inicio":this.value,
          "data_fim":this.value1
        }
        let resultado = await axios.post(process.env.VUE_APP_URL + '/violino_disp',carga);
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
          "id_planta": this.id_planta,
          "data_inicio":this.value,
          "data_fim": this.value1
        }
        let resultado = await axios.post(process.env.VUE_APP_URL + '/dispositivos',carga);
        let resposta = [];
        for(let i=0;i<resultado.data.length;i++){
          resposta.push(resultado.data[i].data)
        }
        // eslint-disable-next-line
        console.log(resposta);
        return resposta;
      },
      printData(){
        // eslint-disable-next-line
        console.log(this.value)
        //this.value = '2020-10-17';

      },
      
      calc_tempo(tempo){
        let dias = (parseInt(tempo/86400));
        let horas = parseInt((tempo % 86400)/3600);
        let texto = dias.toString() + " dias e " + horas.toString() + " horas";
        return texto;
      },
      async att_values(){
          let resultado = await axios.post(process.env.VUE_APP_URL + '/dispositivo',{"id_planta":this.id_planta});
          this.umidade_atual = resultado.data[0].umidade_atual;
          this.tempo_plantado = this.calc_tempo(resultado.data[0].tempo_plantado);
          this.quantidade_agua = resultado.data[0].quantidade_agua;
          for(let i = 0; i<7;i++){
            let resultado_alerta = await axios.post(process.env.VUE_APP_URL + '/dispositivo',{"id_planta":this.id_planta});
            try {
              if(resultado_alerta.data[0].umidade_atual != "" && Number(resultado_alerta.data[0].umidade_atual) < 30 && Number(resultado_alerta.data[0].tempo_plantado) > 7200){
                //alert("Dispositivo de id "+i.toString()+" está com algum defeito");
              }
            } catch (error) {
              // eslint-disable-next-line
              console.log(error);
            }
            
          }
          setTimeout(this.att_values, 3000);
      }
    }
  }
</script>

<style>
.projeto-container{
    display: flex;
}
.small{
  width: 100%;
  height: 50%;
}

</style>
