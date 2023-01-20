# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class PromocaoItem(Executa):
    def __init__(self):
        super().__init__()

    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list:
                if dados_dict['id_promocao_item'] is None:
                    promocao_item_list = None
                else:
                    promocao_item_list = self.select('promocao_item',
                        [
                            "*"
                        ],
                        [
                            "id_promocao_item={}".format(dados_dict['id_promocao_item'])
                        ]
                    )
                
                if promocao_item_list:
                    self.update('promocao_item',
                        [
                            "id_promocao={}".format(dados_dict['id_promocao']),
                            "id_produto={}".format(dados_dict['id_produto']),
                            "minimo={}".format(dados_dict['minimo']),
                            "maximo={}".format(dados_dict['maximo']),
                            "tipo='{}'".format(dados_dict['tipo']),
                            "aplicar='{}'".format(dados_dict['aplicar']),
                            "valor={}".format(dados_dict['valor']),
                        ],
                        [
                            "id_promocao_item={}".format(dados_dict['id_promocao_item'])
                        ]
                    )
                else:
                    self.insert('promocao_item',
                        [
                            'id_promocao',
                            'id_produto',
                            'minimo',
                            'maximo',
                            'tipo',
                            'aplicar',
                            'valor',
                            'id_empresa'
                        ],
                        [
                            "{}".format(dados_dict['id_promocao']),
                            "{}".format(dados_dict['id_produto']),
                            "{}".format(dados_dict['minimo']),
                            "{}".format(dados_dict['maximo']),
                            "'{}'".format(dados_dict['tipo']),
                            "'{}'".format(dados_dict['aplicar']),
                            "{}".format(dados_dict['valor']),
                            "{}".format(dados_dict['id_empresa']),
                        ]
                    )
            return {"Sucesso": "Promoção item inserido ou alterado com sucesso."}

        except KeyError:

            return {"Error": "Parametros inválidos."}