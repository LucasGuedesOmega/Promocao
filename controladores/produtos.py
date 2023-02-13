# -*- coding: UTF-8 -*-
from banco.execucoes import Executa
import re
class Produto(Executa):
    def __init__(self):
        super().__init__()
        
    def insert_ou_update(self, dados_list, auth):

        try:
            retorno_list = []

            for dados_dict in dados_list:
                
                descricao_produtos_list = dados_dict['descricaoProduto'].split(' ')
                descricao_join_list = []
                for p in descricao_produtos_list:
                    palavra = re.sub(r"[^a-zA-Z0-9]","", p)
                    descricao_join_list.append(palavra)

                dados_dict['descricaoProduto'] = " ".join(descricao_join_list)
                
                status_api = dados_dict['status']

                if dados_dict['status'] == 'ATIVO':
                    dados_dict['status'] = 'true'
                else:
                    dados_dict['status'] = 'false'
                
                dados_dict['ncm'] = ''.join(char for char in dados_dict['ncm'] if char.isalnum())

                retorno_produto_dict = {
                    "anp": dados_dict['anp'],
                    "codigoBarras": dados_dict['codigoBarras'],
                    "descricaoProduto": dados_dict['descricaoProduto'],
                    "identificadorExternoProduto": dados_dict['identificadorExternoProduto'],
                    "ncm": dados_dict['ncm'],
                    "status": status_api,
                    "valor": dados_dict['valor']
                }
            
                produto_id = self.select(table='produtos',
                    fields_list=[
                        'id_produto',
                    ],
                    where_list=[
                        "id_externo='{}'".format(dados_dict['identificadorExternoProduto'])
                    ]
                )

                if produto_id:
                    self.update('produtos',
                        [
                            "id_externo='{}'".format(dados_dict['identificadorExternoProduto']),
                            "descricao='{}'".format(dados_dict['descricaoProduto']),
                            "modalidade_produto='{}'".format(dados_dict['modalidadeProduto']),
                            "codigo_empresa='{}'".format(dados_dict['codigoEmpresa']),
                            "token_integracao='{}'".format(dados_dict['tokenIntegracao']),
                            "valor={}".format(dados_dict['valor']),
                            "status={}".format(dados_dict['status']),
                            "codigo_barras='{}'".format(dados_dict['codigoBarras']),
                            "ncm='{}'".format(dados_dict['ncm']),
                            "anp='{}'".format(dados_dict['anp'])
                        ],
                        [
                            "id_externo='{}'".format(dados_dict['identificadorExternoProduto'])
                        ]
                    )
                    retorno_produto_dict['acao'] = "UPDATE"
                else:
                    self.insert('produtos',
                        [
                            'id_externo',
                            'descricao',
                            'modalidade_produto',
                            'codigo_empresa',
                            'token_integracao',
                            'valor',
                            'status',
                            'codigo_barras',
                            'ncm',
                            'anp',
                            'id_empresa',
                            'id_grupo_empresa'
                        ],
                        [
                            "'{}'".format(dados_dict['identificadorExternoProduto']),
                            "'{}'".format(dados_dict['descricaoProduto']),
                            "'{}'".format(dados_dict['modalidadeProduto']),
                            "'{}'".format(dados_dict['codigoEmpresa']),
                            "'{}'".format(dados_dict['tokenIntegracao']),
                            "'{}'".format(dados_dict['valor']),
                            dados_dict['status'],
                            "'{}'".format(dados_dict['codigoBarras']),
                            "'{}'".format(dados_dict['ncm']),
                            "'{}'".format(dados_dict['anp']),
                            "{}".format(auth['id_empresa']),
                            "{}".format(auth['id_grupo_empresa']),
                        ]
                    )
                    retorno_produto_dict['acao'] = "CREATE"
                
                retorno_list.append(retorno_produto_dict)

            return retorno_list
            
        except KeyError:

            return {"Error": "Parametros invalidos"}
