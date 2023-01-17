from flask import Flask, request, jsonify, abort, current_app
import os
from flask_cors import CORS
from functools import wraps
import jwt
import datetime
import time
from base64 import b64decode
import json

from controladores.grupos_pagamento import GrupoPagamento
from controladores.produtos import Produto
from controladores.clientes import Cliente
from controladores.vouchers import Voucher
from controladores.promocoes import Promocao
from controladores.grupos_empresa import GrupoEmpresa
from controladores.empresas import Empresa
from controladores.produtos_avulso import ProdutoAvulso
from controladores.promocao_item import PromocaoItem
from controladores.formas_pagamento import FormaPagamento
from controladores.grupos_forma_pagamento import GrupoFormaPagamento
from controladores.usuarios import Usuario
from controladores.buscar import Busca
from controladores.promocao_empresa import PromocaoEmpresa
from controladores.venda import Venda
from controladores.historico_login import HistoricoLogin
from banco.execucoes import Executa

api = Flask(__name__)
CORS(api, resources={r'/api/v1/*'})
SECRET_KEY = os.urandom(12).hex()
api.config['SECRET_KEY'] = SECRET_KEY

def autenticar_api(f):
    @wraps(f)   
    def decorated(*args, **kwargs):
        current_user = None
        token = None
        if "Authorization" in request.headers:
            if "Basic " in request.headers["Authorization"]:
                token = request.headers["Authorization"].split("Basic ")[1]
            else:
                token = request.headers["Authorization"]

        if not token:
            return {
                "message": "Token de autorização faltando!",
                "data": None,
                "error": "não autorizado"
            }, 401
        try:
            data=jwt.decode(token, b64decode(current_app.config["SECRET_KEY"]), algorithms=["HS256"])
            current_user = Usuario().select('usuarios', ['*'], ["id_usuario={}".format(data['id_usuario'])])
            if current_user is None:
                print('token invalido')
                return {
                    "message": "Token Inválido!",
                    "data": None,
                    "error": "não autorizado"
                }, 401
            if not current_user[0]["status"]:
                print('status')
                abort(403)
        except jwt.exceptions.ExpiredSignatureError:
            print('token expirado')
            return {
                "message": "Algo deu errado",
                "data": None,
                "error": 'Token expirado'
            }, 400
        except jwt.exceptions.InvalidSignatureError:
            return {'erros': ['Sem conexao com a api ou falta fazer login.']}, 400
        except Exception as e:
            print(e)
            return {
                "message": "Algo deu errado",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user[0], *args, **kwargs)

    return decorated

@api.route('/api/v1/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            dados_list = request.get_json()
            for dados_dict in dados_list:
            
                if dados_dict.get('username') and dados_dict.get('senha'):

                    dados_dict['username'] = dados_dict['username'].replace(" ", "")
                    dados_dict['senha'] = dados_dict['senha'].replace(" ", "")

                    usuario = Usuario().select('usuarios', ['id_usuario', 'user_admin', 'id_empresa'], ["username='{}'".format(dados_dict['username']), "senha='{}'".format(dados_dict['senha'])])

                    if usuario:
                        empresa = Empresa().select('empresa', ['id_grupo_empresa'], [f"id_empresa={int(usuario[0]['id_empresa'])}"])
                        payload = None
                        if dados_dict['tipo'] == "app":
                            payload = {
                                "id_usuario": int(usuario[0]['id_usuario']),
                                "id_empresa": int(usuario[0]['id_empresa']),
                                "id_grupo_empresa": int(empresa[0]['id_grupo_empresa']),
                                "iat": (time.mktime(datetime.datetime.now().timetuple())),
                                "exp": (time.mktime((datetime.datetime.now() + datetime.timedelta(days=30)).timetuple())),
                                "admin": usuario[0]['user_admin']
                            }
                        elif dados_dict['tipo'] == 'consumidor':
                            payload = {
                                "id_usuario": int(usuario[0]['id_usuario']),
                                "id_empresa": int(usuario[0]['id_empresa']),
                                "id_grupo_empresa": int(empresa[0]['id_grupo_empresa']),
                                "admin": usuario[0]['user_admin']
                            }
                        else:
                            payload = {
                                "id_usuario": int(usuario[0]['id_usuario']),
                                "id_empresa": int(usuario[0]['id_empresa']),
                                "id_grupo_empresa": int(empresa[0]['id_grupo_empresa']),
                                "iat": (time.mktime(datetime.datetime.now().timetuple())),
                                "exp": (time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=30)).timetuple())),
                                "admin": usuario[0]['user_admin']
                            }

                        if payload:
                            token =  jwt.encode(payload, b64decode(f"{api.config['SECRET_KEY']}"), algorithm='HS256')

                        if dados_dict.get("name_hardware"):
                            data_historico = Executa().format_date(datetime.datetime.now()) + " " + Executa().format_time(datetime.datetime.now())

                            dados_historico_list = [
                                {
                                    "data_ultimo_login": data_historico,
                                    "id_usuario": usuario[0]['id_usuario'],
                                    "name_hardware": dados_dict['name_hardware']
                                }
                            ]

                            HistoricoLogin().insert_ou_update(dados_historico_list)

                        return jsonify({
                            "token": token
                        })
                    else:
                        return jsonify({"Error": "Username ou Senha inválidos."}), 400

                elif dados_dict.get('username') and not dados_dict.get('senha'):
                    return jsonify({"Error": "Informe uma senha."}), 400

                elif not dados_dict.get('username') and dados_dict.get('senha'):
                    return jsonify({"Error": "Informe um username."}), 400

                else:
                    return jsonify({"Error": "Informe username e senha."}), 400

        except Exception as e:
            print(e)
            return jsonify({"Error": "Parametros invalidos"}), 401

@api.route('/api/v1/empresas-promocao', methods=['GET', 'POST'])
@autenticar_api
def promocao_empresas(auth):
    if request.method == 'POST':
        
        dados_list = request.get_json()

        retorno = PromocaoEmpresa().insert_ou_update(dados_list)

        return retorno 

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'promocao_empresas')

        return retorno

@api.route('/api/v1/historico-login', methods=['GET'])
def historico_login():
    if request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = HistoricoLogin().buscar(parametros_dict)

        return retorno

@api.route('/api/v1/login-token', methods=['POST'])
@autenticar_api
def login_token(auth):
    dados_list = request.get_json()
    
    if dados_list.get('token'):
        try:
            data=jwt.decode(dados_list['token'], b64decode(current_app.config["SECRET_KEY"]), algorithms=["HS256"])
            current_user = Usuario().select('usuarios', ['*'], ["id_usuario={}".format(data['id_usuario'])])
            if not current_user:
                return {
                    "message": "Token Inválido!",
                    "data": None,
                    "error": "não autorizado"
                }, 401
            else:
                return current_user, 200

        except jwt.exceptions.ExpiredSignatureError:
            return {
                "message": "Algo deu errado",
                "data": None,
                "error": 'Token expirado'
            }, 500

        except Exception as e:
            return {
                "message": "Algo deu errado",
                "data": None,
                "error": str(e)
            }, 500

@api.route('/api/v1/usuario', methods=['GET', 'POST'])
@autenticar_api
def usuarios(auth):
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = Usuario().insert_ou_update(dados_list)

        return retorno

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'usuarios')

        return retorno

@api.route('/api/v1/integracao/produto/lista', methods=['GET', 'POST'])
@autenticar_api
def produtos(auth):
    if request.method == 'POST':

        dados_list = json.loads(request.data.decode('ISO 8859-1')) 
  
        retorno = Produto().insert_ou_update(dados_list, auth)

        return jsonify(retorno)

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'produtos')

        return retorno

@api.route('/api/v1/cliente', methods=['GET', 'POST'])
@autenticar_api
def cliente(auth):
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = Cliente().insert_ou_update(dados_list)

        return retorno

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'clientes')

        return retorno

@api.route('/api/v1/gera-voucher', methods=['POST'])
@autenticar_api
def gera_voucher(auth):
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = Voucher().insert_ou_update(dados_list, auth)

        return jsonify(retorno)

@api.route('/api/v1/integracao/validarcodigo/lista', methods=['POST'])
@autenticar_api
def validar_voucher(auth):
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = Voucher().valida_codigo(dados_list, auth)

        return retorno

@api.route('/api/v1/vendas', methods=['GET'])
@autenticar_api
def venda(auth):
   
    parametros_dict = request.args.to_dict()

    retorno = Busca().buscar(parametros_dict, auth, 'venda')

    return retorno

@api.route('/api/v1/integracao/posvenda', methods=['GET', 'POST'])
@autenticar_api
def pos_venda(auth):
    if request.method == 'POST':    
        
        dados_dict = request.get_json()

        retorno = Venda().pos_venda(dados_dict, auth)

        return retorno

@api.route('/api/v1/integracao/cancelarvenda', methods=['GET', 'POST'])
@autenticar_api
def cancela_venda(auth):
    if request.method == 'POST':    

        retorno = Venda().cancela_venda(auth)

        return retorno

@api.route('/api/v1/promocao', methods=['GET', 'POST'])
@autenticar_api
def promocao(auth):
    if request.method == 'POST':    

        dados_list = request.get_json()

        retorno = Promocao().insert_ou_update(dados_list)

        return retorno
    
    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'promocao')

        return retorno

@api.route('/api/v1/promocao-item', methods=['GET', 'POST'])
@autenticar_api
def promocao_item(auth):
    if request.method == 'POST':    

        dados_list = request.get_json()

        retorno = PromocaoItem().insert_ou_update(dados_list)

        return retorno

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'promocao_item')

        return retorno

@api.route('/api/v1/grupo-empresa', methods=['GET', 'POST'])
@autenticar_api
def grupo_empresa(auth):
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = GrupoEmpresa().insert_ou_update(dados_list)

        return retorno

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'grupo_empresa')

        return retorno

@api.route('/api/v1/empresa', methods=['GET', 'POST'])
@autenticar_api
def empresa(auth):
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = Empresa().insert_ou_update(dados_list)

        return retorno

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'empresa')

        return retorno

@api.route('/api/v1/grupo-pagamento', methods=['GET', 'POST'])
@autenticar_api
def grupo_pagamento(auth):
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = GrupoPagamento().insert_ou_update(dados_list)

        return retorno

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'grupo_pagamento')

        return retorno

@api.route('/api/v1/produto-avulso', methods=['GET', 'POST'])
@autenticar_api
def produto_avulso(auth):
    if request.method == 'POST':
        
        dados_list = request.get_json()

        retorno = ProdutoAvulso().insert_ou_update(dados_list)

        return retorno 

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'produto_avulso')

        return retorno

@api.route('/api/v1/forma-pagamento', methods=['GET', 'POST'])
@autenticar_api
def forma_pagamento(auth):
    if request.method == 'POST':
        
        dados_list = request.get_json()

        retorno = FormaPagamento().insert_ou_update(dados_list)

        return retorno 

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'forma_pagamento')

        return retorno

@api.route('/api/v1/grupo-forma-pagamento', methods=['GET', 'POST'])
@autenticar_api
def grupo_forma_pagamento(auth):
    if request.method == 'POST':
        
        dados_list = request.get_json()

        retorno = GrupoFormaPagamento().insert_ou_update(dados_list)

        return retorno 

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'grupo_forma_pagamento')

        return retorno

@api.errorhandler(Exception)
def handle_exception(err):
    print(err)
    path = request.path 
    print(path)

if __name__ == '__main__':
    api.run(debug=True, host='192.168.1.18', port=5080)