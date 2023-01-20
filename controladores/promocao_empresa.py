# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class PromocaoEmpresa(Executa):
    def __init__(self):
        super().__init__()

    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list:
                if dados_dict['id_promocao_empresa'] is None:
                    promocao_empresa_list = None
                else:
                    promocao_empresa_list = self.select('promocao_empresas', 
                        [
                            '*'
                        ],
                        [ "id_promocao_empresa={}".format(dados_dict['id_promocao_empresa'])]
                    )
                
                if promocao_empresa_list:

                    self.update("promocao_empresas", 
                        [
                            "id_promocao={}".format(dados_dict['id_promocao']),
                            "id_empresa={}".format(dados_dict['id_empresa']),
                            'status={}'.format(dados_dict['status'])
                        ],
                        [ "id_promocao_empresa={}".format(dados_dict['id_promocao_empresa'])]
                    )
                else:
                    self.insert('promocao_empresas',
                        [
                            "id_promocao",
                            "id_empresa",
                            'id_grupo_empresa',
                            'status'
                        ],
                        [
                            "{}".format(dados_dict['id_promocao']), 
                            "{}".format(dados_dict['id_empresa']), 
                            "{}".format(dados_dict['id_grupo_empresa']), 
                            "{}".format(dados_dict['status']), 
                        ]
                    )

            return {"Sucesso": "Vinculo entre empresa e promoção inserido ou alterado com sucesso."}, 200

        except Exception as e:

            return {"Error": f"Parametros inválidos {e}."}, 400