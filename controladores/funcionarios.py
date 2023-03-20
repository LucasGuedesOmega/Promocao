# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class Funcionario(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list: 

                dados_dict['cpf'] = dados_dict['cpf'].replace('.', '').replace('-', '')

                is_funcionario = False

                dados_funcionario = self.select('funcionario', ['*'], [f"cpf='{dados_dict['cpf']}'"])
                if dados_funcionario:
                    is_funcionario = True
                    
                dados_dict['cpf'] = ''.join(char for char in dados_dict['cpf'] if char.isalnum())
                dados_dict['telefone'] = ''.join(char for char in dados_dict['telefone'] if char.isalnum())
                
                where_list = []

                if dados_dict.get('id_funcionario'):
                    where_list.append("id_funcionario={}".format(dados_dict['id_funcionario']))
                elif dados_dict.get('cpf') and not dados_dict.get('id_funcionario'):
                    where_list.append("cpf='{}'".format(dados_dict['cpf']))

                funcionario_list = self.select('funcionario', 
                    [
                        "id_funcionario"
                    ],
                    where_list  
                )

                if funcionario_list:
                
                    self.update('funcionario',
                        [
                            "nome='{}'".format(dados_dict['nome']),
                            "e_mail='{}'".format(dados_dict['e_mail']),
                            "telefone='{}'".format(dados_dict['telefone']),
                            "status={}".format(dados_dict['status']),
                            "id_usuario={}".format(dados_dict['id_usuario']),
                            "id_empresa={}".format(dados_dict['id_empresa']),
                            "cpf='{}'".format(dados_dict['cpf']),
                        ],
                        where_list  
                    )
                
                else:
                    if not is_funcionario:
                        self.insert('funcionario',
                            [
                                "nome",
                                "cpf",
                                "e_mail",
                                "telefone",
                                "status",
                                "id_empresa",
                                "id_grupo_empresa",
                                'id_usuario'
                            ],
                            [
                                "'{}'".format(dados_dict['nome']),
                                "'{}'".format(dados_dict['cpf']),
                                "'{}'".format(dados_dict['e_mail']),
                                "'{}'".format(dados_dict['telefone']),
                                "{}".format(dados_dict['status']),
                                "{}".format(dados_dict['id_empresa']),
                                "{}".format(dados_dict['id_grupo_empresa']),
                                "{}".format(dados_dict['id_usuario'])
                            ]   
                        )
            
                    else:
                        return {"Error": f"Funcionário já cadastrado"}, 400
                    
            return {"Sucesso": "Funcionario cadastrado com sucesso!"}, 200

        except Exception as e:
            print(e)
            return {"Error": f"Parametros invalidos {e}"}, 400