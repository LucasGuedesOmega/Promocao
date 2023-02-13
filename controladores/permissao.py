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

    def valida_permissao(self, auth):

        permissao_usuario_telas_list = []
   
        if auth.get('user_admin') or auth.get('admin_posto') and not auth.get('id_grupo_usuario'):
            permissao_tela_list = self.select('tela_acao', ['*'])

            for permissao_tela_dict in permissao_tela_list:
                if permissao_tela_dict:

                    tela_dict = {
                        'nome': permissao_tela_dict['nome']
                    }

                    permissao_usuario_telas_list.append(tela_dict)

            return permissao_usuario_telas_list, 200

        grupo_usuario_dict = self.select('grupo_usuario', ['*'], [f"id_grupo_usuario={auth['id_grupo_usuario']}"], registro_unico=True)

        if grupo_usuario_dict:
            
            permissao_tela_list = self.select('permissao_tela_acao', ['*'], [f"id_permissao={grupo_usuario_dict['id_permissao']}"])
            
            for permissao_tela_dict in permissao_tela_list:
                if permissao_tela_dict.get('id_tela_acao'):
                    permissao_usuario_tela_dict = self.select("tela_acao", ['*'], [f"id_tela_acao={permissao_tela_dict['id_tela_acao']}"], registro_unico=True)

                    if permissao_usuario_tela_dict:
                        tela_dict = {
                            'nome': permissao_usuario_tela_dict['nome']
                        }

                        permissao_usuario_telas_list.append(tela_dict)
                else:
                    return {'error': 'Nenhuma ação ou tela configurada para este grupo de usuários.'}, 400

            return permissao_usuario_telas_list, 200
        else:
            return {'error': 'Algo deu errado com o grupo de usuário'}, 400

    def valida_permissao_tela(self, dados_dict, auth):

        if auth.get('user_admin') or auth.get('admin_posto') and not auth.get('id_grupo_usuario'):
            return {'permissao': True, 'cadastro': True, 'editar': True}, 200

        if not dados_dict.get('tela'):
            return {'error': 'informe o parametro tela.'}, 400

        permissao_usuario_telas_list = []

        grupo_usuario_dict = self.select('grupo_usuario', ['*'], [f"id_grupo_usuario={auth['id_grupo_usuario']}"], registro_unico=True)

        if grupo_usuario_dict:
            
            permissao_tela_list = self.select('permissao_tela_acao', ['*'], [f"id_permissao={grupo_usuario_dict['id_permissao']}"])
            
            for permissao_tela_dict in permissao_tela_list:
                if permissao_tela_dict.get('id_tela_acao'):
                    permissao_usuario_tela_dict = self.select("tela_acao", ['*'], [f"id_tela_acao={permissao_tela_dict['id_tela_acao']}"], registro_unico=True)

                    if permissao_usuario_tela_dict:

                        permissao_usuario_telas_list.append(permissao_usuario_tela_dict['nome'])

                else:
                    return {'error': 'Nenhuma ação ou tela configurada para este grupo de usuários.'}, 400
        else:
            return {'error': 'Grupo de usuário não vinculado ao usuário'}, 400

        cadastro = 'CADASTRO'
        editar = 'EDITAR'

        if dados_dict['tela'] in permissao_usuario_telas_list and cadastro in permissao_usuario_telas_list and editar in permissao_usuario_telas_list:
            return {'permissao': True, 'cadastro': True, 'editar': True}, 200
        elif dados_dict['tela'] in permissao_usuario_telas_list and cadastro not in permissao_usuario_telas_list and editar in permissao_usuario_telas_list:
            return {'permissao': True, 'cadastro': False, 'editar': True}, 200
        elif dados_dict['tela'] in permissao_usuario_telas_list and cadastro in permissao_usuario_telas_list and editar not in permissao_usuario_telas_list:
            return {'permissao': True, 'cadastro': True, 'editar': False}, 200
        elif dados_dict['tela'] in permissao_usuario_telas_list and cadastro not in permissao_usuario_telas_list and editar not in permissao_usuario_telas_list:
            return {'permissao': True, 'cadastro': False, 'editar': False}, 200
        else:
            return {'permissao': False}, 200