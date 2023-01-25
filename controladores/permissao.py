# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class Permissao(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):
        
        try:
            for dados_dict in dados_list:
                
                permissao_list = None
                if dados_dict.get('id_permissao'):
                    permissao_list = self.select('permissao', 
                        [
                            '*'
                        ],
                        [
                            'id_permissao={}'.format(dados_dict['id_permissao'])
                        ]
                    )
                
                if permissao_list:
                    self.update('permissao',
                        [
                            "nome='{}'".format(dados_dict['nome']),
                            "status={}".format(dados_dict['status']),
                        ],
                        [
                            "id_permissao={}".format(dados_dict['id_permissao'])
                        ]
                    )
                    
                    return {"Sucesso": "Permissao inserida ou alterada com sucesso.", 'id': dados_dict['id_permissao']}, 200

                else:
                    self.insert('permissao',
                        [
                            "nome",
                            "id_empresa",
                            "id_grupo_empresa",
                            "status",
                        ],
                        [
                            "'{}'".format(dados_dict['nome']),
                            "{}".format(dados_dict['id_empresa']),
                            "{}".format(dados_dict['id_grupo_empresa']),
                            "{}".format(dados_dict['status']),
                        ]
                    )

                    last_permissao = self.select('permissao', ['id_permissao'], ['id_permissao=(select max(id_permissao) from permissao)'], registro_unico=True)

                    return {"Sucesso": "Permissao inserida ou alterada com sucesso.", 'id': last_permissao['id_permissao']}, 200

        except Exception as e:
            
            return {"Error": f"Parametros inválidos {e}."}, 400