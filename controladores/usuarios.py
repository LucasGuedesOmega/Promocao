from banco.execucoes import Executa

class Usuario(Executa):
    def __init__(self):
        super().__init__()

    def insert_historico_login(self, hardware_name):
        pass

    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list: 

                where_list = []

                usuarios_list = None
                if dados_dict.get('id_usuario'):
                    where_list.append("id_usuario={}".format(dados_dict['id_usuario']))

                    usuarios_list = self.select('usuarios', 
                        [
                            "id_usuario"
                        ],
                        where_list  
                    )

                if usuarios_list:
                    self.update('usuarios',
                        [
                            "username='{}'".format(dados_dict['username']),
                            "senha='{}'".format(dados_dict['senha']),
                            "status={}".format(dados_dict['status']),
                            "user_admin={}".format(dados_dict['user_admin']),
                            "id_empresa={}".format(dados_dict['id_empresa']),
                        ],
                        where_list  
                    )

                    return {'Sucesso': 'Usuario cadastro com sucessp', 'id': dados_dict['id_usuario']}, 200

                else:

                    self.insert('usuarios',
                        [
                            "username",
                            "senha",
                            "status",
                            "user_admin",
                            "id_empresa",
                        ],
                        [
                            "'{}'".format(dados_dict['username']),
                            "'{}'".format(dados_dict['senha']),
                            "'{}'".format(dados_dict['status']),
                            "{}".format(dados_dict['user_admin']),
                            "{}".format(dados_dict['id_empresa']),
                        ]   
                    )

                    last_usuario_list = self.select('usuarios', ['id_usuario'], ['id_usuario=(select max(id_usuario) from usuarios)'])
                  
                    return {'Sucesso': 'Usuario cadastro com sucessp', 'id': last_usuario_list[0]['id_usuario']}, 200

        except Exception as e:
            print(e)
            return {"Error": "Parametros invalidos"}, 400