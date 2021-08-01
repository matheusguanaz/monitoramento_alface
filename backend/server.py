from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import helper as hr
import psycopg2
from flask_cors import CORS
import connect as ct


app = Flask(__name__)
api = Api(app)
CORS(app)


class Geral(Resource):
    def get(self):
        resultado = ct.executarSelect("SELECT * FROM dados")
        colunas = ['id_coleta','id_planta','umidade_atual','temperatura','umidade_ar','vazao','quantidade_agua','luminosidade','tempo_plantado']
        resposta = []
        for res in resultado:
            resposta.append(hr.criarJSON(chaves=colunas, valores=res))
        return jsonify(resposta)

class Datas(Resource):
    def get(self):
        resultado = ct.executarSelect("SELECT luminosidade, temperatura, umidade_ar, uv FROM dados order by dat_gravacao desc limit 1")
        colunas = ['luminosidade','temperatura','umidade_ar','uv']
        resposta = []
        for res in resultado:
            resposta.append(hr.criarJSON(chaves=colunas, valores=res))

        return jsonify(resposta)

    def put(self):
        conn = psycopg2.connect(user="postgres",password="123",host="192.168.0.25", port="5432",database="tcc")
        cursor = conn.cursor()
        if(request.json['modo_operacao']=='0' or request.json['modo_operacao']==0):
            if(request.json['qtd_agua']==-1):
                ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 0")
                ct.execUpdateOuInsert("UPDATE plantas SET periodo_rega ="+str(request.json['periodo_rega']))
                ct.execUpdateOuInsert("UPDATE plantas SET tempo_rega="+str(request.json['tempo_rega']))
                ct.execUpdateOuInsert("UPDATE plantas SET qtd_agua = -1")
                ct.execUpdateOuInsert("UPDATE plantas set flag_novo_modo = 1")
            else:
                ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 0")
                ct.execUpdateOuInsert("UPDATE plantas SET periodo_rega ="+ str(request.json['periodo_rega']))
                ct.execUpdateOuInsert("UPDATE plantas SET tempo_rega = 0")
                ct.execUpdateOuInsert("UPDATE plantas SET qtd_agua = "+ request.json['qtd_agua'])  
                ct.execUpdateOuInsert("UPDATE plantas set flag_novo_modo = 1")
        elif(request.json['modo_operacao']=='1'or request.json['modo_operacao']==1):
            ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 1")
            ct.execUpdateOuInsert("UPDATE plantas SET periodo_rega = 300")
            ct.execUpdateOuInsert("UPDATE plantas SET tempo_rega = 0")
        elif (request.json['modo_operacao']=='2'):
            ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 2")




    def post(self):

        if (request.json['data_inicio']==request.json['data_fim']):
            resultado = ct.executarSelect("SELECT avg(" + str(request.json['inf']) + "), to_char(dat_gravacao,'HH24:MI') FROM dados WHERE date(dat_gravacao) ='" + request.json['data_inicio']+"' group by to_char(dat_gravacao,'HH24:MI')")
        else:
            resultado = ct.executarSelect("SELECT " + str(request.json['inf']) + ", date FROM dados_view WHERE date BETWEEN '" + request.json['data_inicio']+"' AND '"+ request.json['data_fim']+"'")
        resposta = []
        colunas = ['valor_medio','data']
        if(request.json['inf']=='uv'):
            novo_resultado = []
            for res in resultado:
                novo_resultado.append([hr.mapperUV(res[0]),res[1]])
            resultado = novo_resultado
        for res in resultado:
            resposta.append(hr.criarJSON(chaves=colunas, valores=res))
        return jsonify(resposta)


class Dispositivos(Resource):

    def post(self):
        resultado = []
        if (request.json['data_inicio']==request.json['data_fim']):
            resultado = ct.executarSelect("SELECT " + str(request.json['inf']) + ", dat_gravacao FROM dados WHERE date(dat_gravacao) ='" + request.json['data_inicio']+"' AND id_planta ="+ request.json['id_planta'])
        else:
            resultado = ct.executarSelect("SELECT avg(" + str(request.json['inf']) + "), date(dat_gravacao) FROM dados WHERE id_planta = "+request.json['id_planta']+" AND date(dat_gravacao) BETWEEN '" + request.json['data_inicio']+"' AND '"+ request.json['data_fim']+"' GROUP BY (date(dat_gravacao))")
            if(request.json['inf']=="quantidade_agua"):
                resultado = ct.executarSelect("SELECT SUM("+ str(request.json['inf']) +"), date(dados.dat_gravacao) FROM dados WHERE id_planta =" + request.json['id_planta'] + " and dat_gravacao between '"+request.json['data_inicio']+ " 00:00:00' and '" + request.json['data_fim']+" 23:59:59' group by date(dados.dat_gravacao) order by date(dados.dat_gravacao)")
        resposta = []
        colunas = ['valor_medio','data']
        for res in resultado:
            resposta.append(hr.criarJSON(chaves=colunas, valores=res))
        return jsonify(resposta)

    def get(self):
        resultado = ct.executarSelect("select id_planta, modo_operacao, periodo_rega, tempo_rega, qtd_agua from plantas order by id_planta")
        resposta = []
        colunas = ['id_planta','modo_operacao','periodo_rega','tempo_rega','qtd_agua']
        for res in resultado:
            resposta.append(hr.criarJSON(chaves=colunas, valores=res))
        return jsonify(resposta)

    def put(self):
        if(request.json['modo_operacao']==2):
            ct.execUpdateOuInsert("UPDATE plantas SET tempo_plantio = 0 WHERE id_planta="+str(request.json['id_planta']))
            ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 2 WHERE id_planta="+str(request.json['id_planta']))

        if(request.json['modo_operacao']==0):
            ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 1 WHERE id_planta="+str(request.json['id_planta']))


class Dispositivo(Resource):

    def post(self):
        resultado = ct.executarSelect("select umidade_atual, tempo_plantado, quantidade_agua from dados WHERE id_planta="+request.json['id_planta']+" AND date(dat_gravacao)=current_date order by dat_gravacao desc limit 1")
        resposta = []
        colunas = ['umidade_atual','tempo_plantado','quantidade_agua']
        for res in resultado:
            resposta.append(hr.criarJSON(chaves=colunas, valores=res))
        return jsonify(resposta)

    def put(self):
        if(request.json['modo_operacao']=='0' or request.json['modo_operacao']==0):
            if(request.json['qtd_agua']==-1):
                ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 0 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
                ct.execUpdateOuInsert("UPDATE plantas SET periodo_rega ="+ str(request.json['periodo_rega'])+" where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
                ct.execUpdateOuInsert("UPDATE plantas SET tempo_rega="+str(request.json['tempo_rega'])+" where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
                ct.execUpdateOuInsert("UPDATE plantas SET qtd_agua = -1 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
                ct.execUpdateOuInsert("UPDATE plantas set flag_novo_modo = 1 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")  
            else:
                ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 0 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
                ct.execUpdateOuInsert("UPDATE plantas SET periodo_rega ="+ str(request.json['periodo_rega'])+" where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
                ct.execUpdateOuInsert("UPDATE plantas SET tempo_rega = 0 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
                ct.execUpdateOuInsert("UPDATE plantas SET qtd_agua = "+ request.json['qtd_agua'] +" where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")  
                ct.execUpdateOuInsert("UPDATE plantas set flag_novo_modo = 1 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")

        elif(request.json['modo_operacao']=='1'or request.json['modo_operacao']==1):
            ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 1 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
            ct.execUpdateOuInsert("UPDATE plantas SET periodo_rega = 300 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
            ct.execUpdateOuInsert("UPDATE plantas SET tempo_rega = 0 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
            ct.execUpdateOuInsert("UPDATE plantas SET qtd_agua = -1 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
            ct.execUpdateOuInsert("UPDATE plantas SET flag_novo_modo = 1 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")  
        elif (request.json['modo_operacao']=='2'):
            ct.execUpdateOuInsert("UPDATE plantas SET modo_operacao = 2 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
            ct.execUpdateOuInsert("UPDATE plantas SET tempo_rega = 0 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")
            ct.execUpdateOuInsert("UPDATE plantas SET flag_novo_modo = 1 where pino_valvula = (select pino_valvula from plantas where id_planta ="+ request.json['id_planta']+")")  
            


        
class Encher(Resource):
    def get(self):
        ct.execUpdateOuInsert("INSERT INTO tempos_vazao(tempo,solenoide,dat_gravacao) VALUES(0,23,current_timestamp)")
        ct.execUpdateOuInsert("INSERT INTO tempos_vazao(tempo,solenoide,dat_gravacao) VALUES(0,26,current_timestamp)")

class Tempos(Resource):
    def get(self):
        result = ct.executarSelect("SELECT tempo FROM tempos_vazao where solenoide=23 order by dat_gravacao desc limit 1")
        try:
            litros = float(result[0][0])
        except:
            litros = 0
        resposta = []
        resposta.append(hr.criarJSON(chaves=['tempos'], valores=[litros]))
        return jsonify(resposta)

class Violino(Resource):
    def post(self):
        resultado = []
        if(request.json['data_inicio']==request.json['data_fim']):
            resultado = ct.executarSelect("SELECT avg(" + str(request.json['inf']) + "), to_char(dat_gravacao,'YYYY-MM-DD HH24:MI') FROM dados WHERE date(dat_gravacao) = '"+request.json['data_inicio']+ "' group by to_char(dat_gravacao,'YYYY-MM-DD HH24:MI')")
        else:
            resultado = ct.executarSelect("SELECT avg(" + str(request.json['inf']) + "), to_char(dat_gravacao,'YYYY-MM-DD HH24:MI') FROM dados WHERE dat_gravacao between '"+request.json['data_inicio']+ " 00:00:00' and '" + request.json['data_fim']+" 23:59:59' group by to_char(dat_gravacao,'YYYY-MM-DD HH24:MI') order by to_char(dat_gravacao,'YYYY-MM-DD HH24:MI')")
        resposta = []
        colunas = ['valor_medio','data']
        if(request.json['inf']=='uv'):
            novo_resultado = []
            for res in resultado:
                novo_resultado.append([hr.mapperUV(res[0]),res[1]])
            resultado = novo_resultado
        for res in resultado:
            resposta.append(hr.criarJSON(chaves=colunas, valores=res))
        return jsonify(resposta)


class ViolinoDisp(Resource):
    def post(self):
        resultado = []
        if (request.json['data_inicio']==request.json['data_fim']):
            resultado = ct.executarSelect("SELECT " + str(request.json['inf']) + ", to_char(dat_gravacao,'YYYY-MM-DD HH24:MI') FROM dados WHERE date(dat_gravacao) ='" + request.json['data_inicio']+"' AND id_planta ="+ request.json['id_planta'])
        else:
            resultado = ct.executarSelect("SELECT " + str(request.json['inf']) + ", to_char(dat_gravacao,'YYYY-MM-DD HH24:MI') FROM dados WHERE id_planta =" + request.json['id_planta'] + " and dat_gravacao between '"+request.json['data_inicio']+ " 00:00:00' and '" + request.json['data_fim']+" 23:59:59' order by dat_gravacao")
        resposta = []
        colunas = ['valor_medio','data']
        
        for res in resultado:
            resposta.append(hr.criarJSON(chaves=colunas, valores=res))
        return jsonify(resposta)

api.add_resource(Violino,'/violino')
api.add_resource(ViolinoDisp,'/violino_disp')
api.add_resource(Geral, '/geral')
api.add_resource(Datas,'/datas') 
api.add_resource(Dispositivos, '/dispositivos')
api.add_resource(Dispositivo,'/dispositivo') 
api.add_resource(Encher,'/encher') 
api.add_resource(Tempos,'/tempos')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="", port=5000)

