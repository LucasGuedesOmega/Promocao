# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class Cliente(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list: 

                dados_dict['cpf'] = dados_dict['cpf'].replace('.', '').replace('-', '')

                is_cliente = False

                dados_cliente = self.select('clientes', ['*'], [f"cpf='{dados_dict['cpf']}'"])
                if dados_cliente:
                    is_cliente = True
                    
                dados_dict['cpf'] = ''.join(char for char in dados_dict['cpf'] if char.isalnum())
                dados_dict['telefone'] = ''.join(char for char in dados_dict['telefone'] if char.isalnum())
                
                where_list = []

                if dados_dict.get('id_cliente'):
                    where_list.append("id_cliente={}".format(dados_dict['id_cliente']))
                elif dados_dict.get('cpf') and not dados_dict.get('id_cliente'):
                    where_list.append("cpf='{}'".format(dados_dict['cpf']))

                cliente_list = self.select('clientes', 
                    [
                        "id_cliente"
                    ],
                    where_list  
                )

                if cliente_list:
                
                    self.update('clientes',
                        [
                            "nome='{}'".format(dados_dict['nome']),
                            "e_mail='{}'".format(dados_dict['e_mail']),
                            "telefone='{}'".format(dados_dict['telefone']),
                            "status={}".format(dados_dict['status']),
                            "cpf='{}'".format(dados_dict['cpf']),
                        ],
                        where_list  
                    )
                
                else:
                    if not is_cliente:
                        self.insert('clientes',
                            [
                                "nome",
                                "cpf",
                                "e_mail",
                                "telefone",
                                "status",
                                "id_grupo_empresa",
                                'id_usuario'
                            ],
                            [
                                "'{}'".format(dados_dict['nome']),
                                "'{}'".format(dados_dict['cpf']),
                                "'{}'".format(dados_dict['e_mail']),
                                "'{}'".format(dados_dict['telefone']),
                                "{}".format(dados_dict['status']),
                                "{}".format(dados_dict['id_grupo_empresa']),
                                "{}".format(dados_dict['id_usuario'])
                            ]   
                        )
            
                    else:
                        return {"Error": f"Cliente já cadastrado"}, 400
                    
                    
            return {"Sucesso": "Cliente cadastrado com sucesso!"}, 200

        except Exception as e:
            print(e)
            return {"Error": f"Parametros invalidos {e}"}, 400