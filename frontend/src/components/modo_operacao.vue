<template>
<div>
    <div class="alinhar">
      <h2>Modo de Operação</h2>
      <b-form-group>
      <b-form-radio v-model="selected" name="some-radios" value=2>Pausado</b-form-radio>
      <b-form-radio v-model="selected" name="some-radios" value=1>Automático</b-form-radio>
      <b-form-radio v-model="selected" name="some-radios" value=0>Manual</b-form-radio>
      <div v-if="selected==0">
        <b-col sm="4">
        <div class="projeto-container">
          Periodo Rega
        <b-form-input v-model="field1" placeholder=""  width="30px"></b-form-input>
         <b-dropdown id="dropdown-3" :text="this.nome" class="m-md-2">
            <b-dropdown-item @click="consPeriodo(1)" >Seg</b-dropdown-item>
            <b-dropdown-item @click="consPeriodo(60)">Min</b-dropdown-item>
            <b-dropdown-item @click="consPeriodo(3600)">Hor</b-dropdown-item>
            <b-dropdown-item @click="consPeriodo(86400)">Dias</b-dropdown-item>
          </b-dropdown>
        </div>
        </b-col>
        <br>
        <b-col sm="3"> 
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
      <b-button @click="setModOperacao(selected)" class="classe-button">Definir</b-button>
    </b-form-group>
    </div>
    </div>
</template>

<script>
import axios from 'axios';


export default {
    data (){
        return {
        selected: 4,
        field1: '',
        field2: '',
        expected: '',
        links1:["Dashboard","Dispositivos","Modo de Operação"],
        vlrPeriodo: null,
        vlrTempo: null,
        nome: 'Seg',
        nome1: 'Seg',
        qtd_agua: -1,
        links: [],
        fields: [
          {
              key: 'id_planta'
          },
          {
              key: 'visualizar',
              label: ''
          }
        ]
      }
    },
    methods:{
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
        async setModOperacao(mod_operacao){
        let carga ={
          "modo_operacao":mod_operacao,
          "periodo_rega":(this.vlrPeriodo === null ? this.field1 : this.vlrPeriodo),
          "tempo_rega":(this.vlrTempo === null ? this.field2 : this.vlrTempo),
          "qtd_agua" : this.qtd_agua
        };
        await axios.put(process.env.VUE_APP_URL + '/datas',carga)
      }
    }
}
</script>

<style>

.classe-link{
    font-size: 150%;
    text-decoration: none;
    color: white;
}
.classe-link:hover{
    cursor: pointer;
    text-decoration: none;
    color: white;
}
.classe-link.active{
    cursor: pointer;
    color: white;
}
.azul1{
    background: #50beda;
    padding-left: 10px;
}
.alinhar{
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 88%;
  height: 80%;
}
</style>