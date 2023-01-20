# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class GrupoEmpresa(Executa):
    def __init__(self):
        super().__init__()

    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list:
                if dados_dict['id_grupo_empresa'] is None:

                    grupo_empresas_list = None

                else:
                    
                    grupo_empresas_list = self.select('grupo_empresa', 
                        ['descricao'],
                        ["id_grupo_empresa='{}'".format(dados_dict['id_grupo_empresa'])]
                    )

                if grupo_empresas_list:
                    self.update('grupo_empresa',
                        ["descricao='{}'".format(dados_dict['descricao']), "status={}".format(dados_dict['status'])],
                        ["id_grupo_empresa='{}'".format(dados_dict['id_grupo_empresa'])]
                    )
                else:
                    self.insert('grupo_empresa',
                        ['descricao', 'status'],
                        ["'{}'".format(dados_dict['descricao']), "{}".format(dados_dict['status'])]
                    )

            return {"Sucesso": "Grupo de empresa cadastrado com sucesso!"}

        except KeyError:

            return {'Error': 'Parametros inválidos.'}