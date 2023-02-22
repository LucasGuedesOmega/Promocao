# -*- coding: UTF-8 -*-
from banco.execucoes import Executa
from controladores.buscar import Busca
class Venda(Executa):
    def __init__(self):
        super().__init__()
    
    def pos_venda(self, dados_dict, auth):
        try:
            ultima_venda_dict = self.select('venda', ['max(id_venda)'], [f"id_usuario={auth['id_usuario']}"], registro_unico=True)
        
            if ultima_venda_dict: 
                self.update('venda',
                    [f"status_venda='CONCLUIDA'"],
                    [f"id_venda={ultima_venda_dict['max(id_venda)']}"]
                )

            return {'Sucesso': 'Pos venda feita com sucesso!'}

        except Exception as e:
            print(e)
            return {'erros': ['Parametros invalidos']}, 400

    def cancela_venda(self, auth):
        try:
            ultima_venda_dict = self.select('venda', ['max(id_venda)'], [f"id_grupo_empresa={auth['id_grupo_empresa']}"])
        
            if ultima_venda_dict: 
                self.update('venda',
                    [f"status_venda='CANCELADA'"],
                    [f"id_venda={ultima_venda_dict['max(id_venda)']}"]
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
                            "status_venda='{}'".format(dados_dict['status_venda']),
                            "tipo_desconto='{}'".format(dados_dict['tipo_desconto']),
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
                            'status_venda',
                            'tipo_desconto',
                            'id_grupo_empresa',
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
                            "'{}'".format(dados_dict['status_venda']),
                            "'{}'".format(dados_dict['tipo_desconto']),
                            "'{}'".format(dados_dict['id_grupo_empresa']),
                        ]   
                    )

            return {"Sucesso": "Venda inserida com sucesso!"}, 200

        except Exception as e:
            print(e)
            return {"Error": "Parametros invalidos"}, 400
    
    def relatorio(self, parametros, auth):
        if auth.get('id_usuario') and auth.get('id_grupo_empresa'):
            
            chave_list = []
            valor_list = list(parametros.values())

            for chave in parametros.keys():
                chave_list.append(chave)

            where_list = Busca().parametros(chave_list, valor_list)[0]

            if where_list:
                where_list[-1] = where_list[-1] + ' order by ve.data_venda, ve.hora_venda'
        
            join_list = [
                "left join produtos p on (ve.id_produto=p.id_produto)",
                "left join forma_pagamento fp on (ve.id_forma_pagamento=fp.id_forma_pagamento)",
                "left join empresa e on (ve.id_empresa=e.id_empresa)",
                "left join promocao pr on (ve.id_promocao=pr.id_promocao)",
            ]

            venda_list = self.select('venda', 
                [
                    've.id_venda', 
                    'p.descricao', 
                    'pr.titulo',
                    'e.razao_social', 
                    'fp.descricao as descricao_forma_pagamento', 
                    've.valor', 
                    've.desconto',
                    've.desconto_unidade',
                    've.quantidade', 
                    've.data_venda', 
                    've.hora_venda'
                ],
                 where_list, join_list)

            return venda_list