# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class HistoricoLogin(Executa):
    def __init__(self):
        super().__init__()
    
    def buscar(self, parametros_dict):
        
        if not parametros_dict.get('name_hardware'):
            return {'Error': "informe a tag 'name_hardware'!"}, 400

        historicos_list = self.select('historico_login', ['*'], [f"name_hardware='{parametros_dict['name_hardware']}' order by data_ultimo_login desc limit 1"], format_date=False)

        return historicos_list, 200
    
    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list:
               
                self.insert('historico_login',
                    [
                        "data_ultimo_login",
                        "id_usuario",
                        "id_empresa",
                        "id_grupo_empresa",
                        "name_hardware",
                    ],
                    [
                        "'{}'".format(dados_dict['data_ultimo_login']),
                        "{}".format(dados_dict['id_usuario']),
                        "{}".format(dados_dict['id_empresa']),
                        "{}".format(dados_dict['id_grupo_empresa']),
                        "'{}'".format(dados_dict['name_hardware']),
                    ]
                )

                last_historico_login = self.select('historico_login', ['id_historico_login'], ['id_historico_login=(select max(id_historico_login) from historico_login)'], registro_unico=True)

                return {"Sucesso": "Historico de login inserido com sucesso.", 'id': last_historico_login['id_historico_login']}, 200

        except Exception as e:
            
            return {"Error": f"Parametros invalidos {e}."}, 400