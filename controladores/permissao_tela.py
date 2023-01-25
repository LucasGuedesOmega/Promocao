# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class PermissaoTela(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):
        try:
            for dados_dict in dados_list:
                if dados_dict['tipo'] == 'I':
                    permissao_tela_acao_list = self.select('permissao_tela_acao', 
                        [
                            '*'
                        ],
                        [
                            'id_tela_acao={}'.format(dados_dict['id_tela_acao']),
                            'id_permissao={}'.format(dados_dict['id_permissao'])
                        ]
                    )
                    
                    if permissao_tela_acao_list:
                    
                        self.update('permissao_tela_acao',
                                [
                                    "id_permissao={}".format(dados_dict['id_permissao']),
                                    "id_tela_acao={}".format(dados_dict['id_tela_acao']),
                                ],
                                [
                                    'id_tela_acao={}'.format(dados_dict['id_tela_acao']),
                                    'id_permissao={}'.format(dados_dict['id_permissao'])
                                ]
                            )

                    else:
                        self.insert('permissao_tela_acao',
                            [
                                "id_permissao",
                                "id_tela_acao",
                            ],
                            [
                                "{}".format(dados_dict['id_permissao']),
                                "{}".format(dados_dict['id_tela_acao']),
                            ]
                        )

                elif dados_dict['tipo'] == 'D':
                    self.delete('permissao_tela_acao', 
                        [
                            "id_permissao={}".format(dados_dict['id_permissao']),
                            "id_tela_acao={}".format(dados_dict['id_tela_acao']),
                        ]
                    )
                
            return {"Sucesso": "Permissao da tela inserida ou alterada com sucesso."}, 200


        except Exception as e:
            
            return {"Error": f"Parametros invalidos {e}."}, 400