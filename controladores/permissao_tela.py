# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class PermissaoTela(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):
        try:
            for dados_dict in dados_list:
                
                permissao_tela_list = None
                if dados_dict.get('id_permissao_tela'):
                    permissao_tela_list = self.select('permissao_tela', 
                        [
                            '*'
                        ],
                        [
                            'id_permissao_tela={}'.format(dados_dict['id_permissao_tela'])
                        ]
                    )
                
                if permissao_tela_list:
                    self.update('permissao_tela',
                        [
                            "id_permissao={}".format(dados_dict['id_permissao']),
                            "id_tela={}".format(dados_dict['id_tela']),
                        ],
                        [
                            "id_permissao_tela={}".format(dados_dict['id_permissao_tela'])
                        ]
                    )
                    
                    return {"Sucesso": "Permissao da tela inserida ou alterada com sucesso.", 'id': dados_dict['id_permissao_tela']}, 200

                else:
                    self.insert('permissao_tela',
                        [
                            "id_permissao",
                            "id_tela",
                        ],
                        [
                            "{}".format(dados_dict['id_permissao']),
                            "{}".format(dados_dict['id_tela']),
                        ]
                    )

                    last_permissao_tela = self.select('permissao_tela', ['id_permissao_tela'], ['id_permissao_tela=(select max(id_permissao_tela) from permissao_tela)'])

                    return {"Sucesso": "Permissao da tela inserida ou alterada com sucesso.", 'id': last_permissao_tela[0]['id_permissao_tela']}, 200

        except Exception as e:
            
            return {"Error": f"Parametros invalidos {e}."}, 400