# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class GrupoUsuario(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_or_update(self, dados_list):

        try:
            for dados_dict in dados_list:
                
                grupo_usuario_list = None
                if dados_dict.get('id_grupo_usuario'):
                    grupo_usuario_list = self.select('grupo_usuario', 
                        [
                            '*'
                        ],
                        [
                            'id_grupo_usuario={}'.format(dados_dict['id_grupo_usuario'])
                        ]
                    )
                
                if grupo_usuario_list:
                    self.update('grupo_usuario',
                        [
                            "nome='{}'".format(dados_dict['nome']),
                            "id_permissao={}".format(dados_dict['id_permissao']),
                        ],
                        [
                            "id_grupo_usuario={}".format(dados_dict['id_grupo_usuario'])
                        ]
                    )
                    
                    return {"Sucesso": "Grupo de usuario inserido ou alterado com sucesso.", 'id': dados_dict['id_grupo_usuario']}, 200

                else:
                    self.insert('grupo_usuario',
                        [
                            "nome",
                            "id_permissao",
                            "id_empresa",
                            "id_grupo_empresa",
                        ],
                        [
                            "'{}'".format(dados_dict['nome']),
                            "{}".format(dados_dict['id_permissao']),
                            "{}".format(dados_dict['id_empresa']),
                            "{}".format(dados_dict['id_grupo_empresa']),
                        ]
                    )

                    last_grupo_usuario = self.select('grupo_usuario', ['id_grupo_usuario'], ['id_grupo_usuario=(select max(id_grupo_usuario) from grupo_usuario)'])

                    return {"Sucesso": "Grupo de usuario inserido ou alterado com sucesso.", 'id': last_grupo_usuario[0]['id_grupo_usuario']}, 200

        except Exception as e:
            
            return {"Error": f"Parametros inválidos {e}."}, 400