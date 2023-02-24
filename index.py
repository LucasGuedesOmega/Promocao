# -*- coding: UTF-8 -*-
from flask import Flask, request, jsonify, abort, current_app, send_from_directory, send_file
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
from controladores.envia_emails import EnviaEmail
from controladores.permissao import Permissao
from controladores.permissao_tela import PermissaoTela
from controladores.grupo_usuario import GrupoUsuario
from controladores.funcionarios import Funcionario
from controladores.exportar import Exportar

from banco.execucoes import Executa

from flask_mail import Mail

api = Flask(__name__)
mail = Mail(api)

api.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
api.config['MAIL_PORT'] = '587'
api.config['MAIL_USERNAME'] = 'lucas_guidolinguedes@outlook.com'
api.config['MAIL_PASSWORD'] = 'lucasgg21121998'
api.config['MAIL_USE_TLS'] = True
api.config['MAIL_USE_SSL'] = False

mail = Mail(api)

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
            current_user = Usuario().select('usuarios', ['*'], ["id_usuario={}".format(data['id_usuario'])], registro_unico=True)
            if current_user is None:
                return {
                    "message": "Token Inválido!",
                    "data": None,
                    "error": "não autorizado"
                }, 401
            if not current_user["status"]:
                abort(403)
        except jwt.exceptions.ExpiredSignatureError:
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

        return f(current_user, *args, **kwargs)

    return decorated

@api.route('/api/v1/login', methods=['POST'])
def login():
    if request.method == 'POST':
        dados_list = request.get_json()
        for dados_dict in dados_list:
        
            if dados_dict.get('username') and dados_dict.get('senha'):

                dados_dict['username'] = dados_dict['username'].replace(" ", "")
                dados_dict['senha'] = dados_dict['senha'].replace(" ", "")

                usuario = Usuario().select('usuarios', 
                [
                    'id_usuario', 
                    'user_admin', 
                    'user_app', 
                    'id_grupo_empresa', 
                    'id_grupo_usuario',
                    'admin_posto'
                ], 
                [
                    "username='{}'".format(dados_dict['username']), 
                    "senha='{}'".format(dados_dict['senha'])
                ], 
                registro_unico=True)

                if usuario:
                    confirma_email_list = Usuario().select('confirma_email', ['*'], [f"id_usuario={usuario['id_usuario']}"])

                    if not confirma_email_list and not usuario['user_admin']:
                        payload = None
                        if dados_dict['tipo'] == "app":
                            payload = {
                                "id_usuario": int(usuario['id_usuario']),
                                "id_grupo_empresa": int(usuario['id_grupo_empresa']),
                                "iat": (time.mktime(datetime.datetime.now().timetuple())),
                                "exp": (time.mktime((datetime.datetime.now() + datetime.timedelta(days=30)).timetuple())),
                                "admin": usuario['user_admin'],
                                "admin_posto": usuario['admin_posto']
                            }
                        elif dados_dict['tipo'] == 'consumidor':
                            payload = {
                                "id_usuario": int(usuario['id_usuario']),
                                "id_grupo_empresa": int(usuario['id_grupo_empresa']),
                                "admin": usuario['user_admin'],
                                "admin_posto": usuario['admin_posto']
                            }
                        else:
                            payload = {
                                "id_usuario": int(usuario['id_usuario']),
                                "id_grupo_empresa": int(usuario['id_grupo_empresa']),
                                "iat": (time.mktime(datetime.datetime.now().timetuple())),
                                "exp": (time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=30)).timetuple())),
                                "admin": usuario['user_admin'],
                                "admin_posto": usuario['admin_posto'],
                            }

                        if usuario.get('id_grupo_usuario') and usuario['id_grupo_usuario']:
                            payload['id_grupo_usuario'] = usuario['id_grupo_usuario']

                        if payload:
                            token =  jwt.encode(payload, b64decode(f"{api.config['SECRET_KEY']}"), algorithm='HS256')

                        if dados_dict.get("name_hardware"):
                            data_historico = Executa().format_date(datetime.datetime.now()) + " " + Executa().format_time(datetime.datetime.now())

                            dados_historico_list = [
                                {
                                    "data_ultimo_login": data_historico,
                                    "id_usuario": usuario['id_usuario'],
                                    "name_hardware": dados_dict['name_hardware']
                                }
                            ]

                            HistoricoLogin().insert_ou_update(dados_historico_list)

                        if usuario['user_app'] == True and dados_dict['tipo'] == 'portal' and not usuario['admin_posto']:
                            return jsonify({"Error": "não autorizado"}), 400
                        
                        if usuario['user_app'] == False and dados_dict['tipo'] == 'app' and not usuario['admin_posto']:
                            return jsonify({"Error": "não autorizado"}), 400

                        return jsonify({
                            "token": token
                        })

                    elif usuario['user_admin']:
                        
                        payload = {
                            "id_usuario": int(usuario['id_usuario']),
                            "admin": usuario['user_admin'],
                            "iat": (time.mktime(datetime.datetime.now().timetuple())),
                            "exp": (time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=30)).timetuple())),
                            "admin_posto": usuario['admin_posto']
                        }

                        if usuario.get('id_grupo_empresa'):
                            payload['id_grupo_empresa'] = usuario['id_grupo_empresa']

                        if usuario.get('id_grupo_usuario'):
                            payload['id_grupo_usuario'] = usuario['id_grupo_usuario']

                        if payload:
                            token =  jwt.encode(payload, b64decode(f"{api.config['SECRET_KEY']}"), algorithm='HS256')

                        return jsonify({
                            "token": token
                        })

                    elif confirma_email_list:
                        return jsonify({"Error": "Email não confirmado."}), 400

                elif not usuario:
                    return jsonify({"Error": "Usuário ou Senha inválidos."}), 400

            elif dados_dict.get('username') and not dados_dict.get('senha'):
                return jsonify({"Error": "Informe uma senha."}), 400

            elif not dados_dict.get('username') and dados_dict.get('senha'):
                return jsonify({"Error": "Informe um usuário."}), 400

            elif not dados_dict.get('username') and not dados_dict.get('senha'):
                return jsonify({"Error": "Informe um usuário e uma senha."}), 400

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

@api.route('/api/v1/usuario', methods=['POST'])
def post_usuarios():
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = Usuario().insert_ou_update(dados_list)

        return retorno

@api.route('/api/v1/usuario', methods=['GET'])
@autenticar_api
def get_usuarios(auth):
    if request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'usuarios')

        return retorno

@api.route('/api/v1/grupo-usuario', methods=['GET', 'POST'])
@autenticar_api
def grupo_usuario(auth):
    if request.method == 'POST':

        dados_list = json.loads(request.data.decode('ISO 8859-1')) 
  
        retorno = GrupoUsuario().insert_ou_update(dados_list)

        return jsonify(retorno)

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'grupo_usuario')

        return retorno
        
@api.route('/api/v1/valida-permissao', methods=['GET'])
@autenticar_api
def valida_permissao(auth):
    if request.method == 'GET':

        retorno = Permissao().valida_permissao(auth)
        
        return retorno

@api.route('/api/v1/valida-permissao-tela', methods=['POST'])
@autenticar_api
def valida_permissao_tela(auth):
    if request.method == 'POST':
        
        dados_dict = request.get_json()

        retorno = Permissao().valida_permissao_tela(dados_dict, auth)
        
        return jsonify(retorno)

@api.route('/api/v1/permissao', methods=['GET', 'POST'])
@autenticar_api
def permissao(auth):
    if request.method == 'POST':

        dados_list = json.loads(request.data.decode('ISO 8859-1')) 
  
        retorno = Permissao().insert_ou_update(dados_list)

        return jsonify(retorno)

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'permissao')
  
        return retorno

@api.route('/api/v1/permissao-tela', methods=['GET', 'POST'])
@autenticar_api
def permissao_tela(auth):
    if request.method == 'POST':

        dados_list = json.loads(request.data.decode('ISO 8859-1')) 
  
        retorno = PermissaoTela().insert_ou_update(dados_list)

        return jsonify(retorno)

    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'permissao_tela_acao')

        return retorno

@api.route('/api/v1/tela-acao', methods=['GET'])
@autenticar_api
def telas(auth):
    if request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'tela_acao')

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

@api.route('/api/v1/cliente', methods=['POST'])
def post_cliente():
    if request.method == 'POST':

        dados_list = request.get_json()

        retorno = Cliente().insert_ou_update(dados_list)

        return retorno

@api.route('/api/v1/cliente', methods=['GET'])
@autenticar_api
def get_cliente(auth):
    if request.method == 'GET':

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

    return jsonify(retorno)

@api.route('/api/v1/relatorio-vendas', methods=['GET'])
@autenticar_api
def relatorio_venda(auth):
   
    parametros_dict = request.args.to_dict()

    retorno = Venda().relatorio(parametros_dict, auth)

    return jsonify(retorno)

@api.route('/api/v1/exporta-excel', methods=['POST'])
@autenticar_api
def exporta_excel(auth):
    if request.method == 'POST':
        dados_list = request.get_json()

        Exportar().exporta_excel(dados_list)

        uploads = os.path.join(current_app.root_path, "static\\arquivos_exportar\\")
        path = 'exportar.xlsx'

        return send_file(uploads+path)

@api.route('/api/v1/exporta-pdf', methods=['POST'])
@autenticar_api
def exporta_pdf(auth):
    if request.method == 'POST':
        dados_list = request.get_json()

        Exportar().exporta_pdf(auth, dados_list)

        uploads = os.path.join(current_app.root_path, "static\\arquivos_exportar\\")
        path = 'exportar.pdf'

        return send_file(uploads+path)

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

@api.route('/api/v1/funcionario', methods=['GET', 'POST'])
@autenticar_api
def funcionario(auth):
    if request.method == 'POST':    

        dados_list = request.get_json()

        retorno = Funcionario().insert_ou_update(dados_list)

        return retorno
    
    elif request.method == 'GET':

        parametros_dict = request.args.to_dict()

        retorno = Busca().buscar(parametros_dict, auth, 'funcionario')

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

@api.route('/api/v1/envia-email', methods=['POST'])
def envia_email():
    if request.method == 'POST':
        
        dados_list = request.get_json()

        retorno = EnviaEmail(mail).envia_email(dados_list)

        return retorno

@api.route('/api/v1/confirma-email', methods=['POST'])
def confirma_email():
    if request.method == 'POST':
        dados_list = request.get_json()

        retorno = EnviaEmail(mail).confirmacao_codigo(dados_list)

        return retorno

@api.errorhandler(Exception)
def handle_exception(err):
    print(err)
    path = request.path 
    print(path)

@api.errorhandler(404)
def page_not_found(error):
    print(error)
    return 'Page not found, 400', 404

if __name__ == '__main__':
    api.run(debug=True, host='172.19.10.30', port=5080)