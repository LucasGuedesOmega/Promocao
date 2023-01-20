# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class Venda(Executa):
    def __init__(self):
        super().__init__()
    
    def pos_venda(self, dados_dict, auth):
        try:
            print(dados_dict)
            ultima_venda_list = self.select('venda', ['max(id_venda)'], [f"id_usuario={auth['id_usuario']}"])
        
            if ultima_venda_list: 
                self.update('venda',
                    [f"status_venda='CONCLUIDA'"],
                    [f"id_venda={ultima_venda_list[0]['max(id_venda)']}"]
                )

            return {'Sucesso': 'Pos venda feita com sucesso!'}

        except Exception as e:
            print(e)
            return {'erros': ['Parametros invalidos']}, 400


    def cancela_venda(self, auth):
        try:
            ultima_venda_list = self.select('venda', ['max(id_venda)'], [f"id_usuario={auth['id_usuario']}"])
        
            if ultima_venda_list: 
                self.update('venda',
                    [f"status_venda='CANCELADA'"],
                    [f"id_venda={ultima_venda_list[0]['max(id_venda)']}"]
                )

            return {'Sucesso': 'Venda cancelada!'}

        except Exception as e:
            print(e)
            return {'erros': ['Parametros invalidos']}, 400

    def insert_or_update(self, dados_list):
        try:
            for dados_dict in dados_list: 

                where_list = []

                venda_list = None
                if dados_dict.get('id_venda'):
                    where_list.append("id_venda={}".format(dados_dict['id_venda']))

                    venda_list = self.select('venda', 
                        [
                            "*"
                        ],
                        where_list  
                    )

                if venda_list:
                    self.update('venda',
                        [
                            "id_produto={}".format(dados_dict['id_produto']),
                            "valor={}".format(dados_dict['valor']),
                            "valor_unidade={}".format(dados_dict['valor_unidade']),
                            "desconto={}".format(dados_dict['desconto']),
                            "desconto_unidade={}".format(dados_dict['desconto_unidade']),
                            "quantidade={}".format(dados_dict['quantidade']),
                            "token_integracao='{}'".format(dados_dict['token_integracao']),
                            "data_venda='{}'".format(dados_dict['data_venda']),
                            "hora_venda='{}'".format(dados_dict['hora_venda']),
                            "id_forma_pagamento={}".format(dados_dict['id_forma_pagamento']),
                            "contigencia={}".format(dados_dict['contigencia']),
                            "id_promocao={}".format(dados_dict['id_promocao']),
                            "id_empresa={}".format(dados_dict['id_empresa']),
                            "id_usuario={}".format(dados_dict['id_usuario']),
                            "descricao_forma_pagamento='{}'".format(dados_dict['descricao_forma_pagamento']),
                            "status_venda='{}'".format(dados_dict['status_venda'])
                        ],
                        where_list  
                    )
                
                else:

                    self.insert('venda',
                        [
                            "id_produto",
                            "valor",
                            "valor_unidade",
                            "desconto",
                            "desconto_unidade",
                            "quantidade",
                            "token_integracao",
                            "data_venda",
                            "hora_venda",
                            "id_forma_pagamento",
                            "contigencia",
                            "id_promocao",
                            "id_empresa",
                            "id_usuario",
                            "descricao_forma_pagamento",
                            'status_venda'
                        ],
                        [
                            "{}".format(dados_dict['id_produto']),
                            "{}".format(dados_dict['valor']),
                            "{}".format(dados_dict['valor_unidade']),
                            "{}".format(dados_dict['desconto']),
                            "{}".format(dados_dict['desconto_unidade']),
                            "{}".format(dados_dict['quantidade']),
                            "'{}'".format(dados_dict['token_integracao']),
                            "'{}'".format(dados_dict['data_venda']),
                            "'{}'".format(dados_dict['hora_venda']),
                            "{}".format(dados_dict['id_forma_pagamento']),
                            "{}".format(dados_dict['contigencia']),
                            "{}".format(dados_dict['id_promocao']),
                            "{}".format(dados_dict['id_empresa']),
                            "{}".format(dados_dict['id_usuario']),
                            "'{}'".format(dados_dict['descricao_forma_pagamento']),
                            "'{}'".format(dados_dict['status_venda'])
                        ]   
                    )

            return {"Sucesso": "Venda inserida com sucesso!"}, 200

        except Exception as e:
            print(e)
            return {"Error": "Parametros invalidos"}, 400