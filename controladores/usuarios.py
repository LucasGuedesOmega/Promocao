from banco.execucoes import Executa

class Usuario(Executa):
    def __init__(self):
        super().__init__()

    def insert_historico_login(self, hardware_name):
        pass

    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list: 
                
                is_cliente = False
                is_usuario = False

                dados_dict['username'] = dados_dict['username'].lower()

                if dados_dict.get('cpf'):
                    dados_dict['cpf'] = dados_dict['cpf'].replace('.', '').replace('-', '')
                    dados_cliente = self.select('clientes', ['*'], [f"cpf='{dados_dict['cpf']}'"])
                    if dados_cliente:
                        is_cliente = True
                
                dados_cliente = self.select('usuarios', ['*'], [f"username = '{dados_dict['username']}'"])
                if dados_cliente:
                    is_usuario = True

                if not is_cliente and not is_usuario:
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
                                "user_app={}".format(dados_dict['user_app']),
                                "id_empresa={}".format(dados_dict['id_empresa'])
                            ],
                            where_list  
                        )

                        return {'Sucesso': 'Usuario cadastro com sucesso', 'id': dados_dict['id_usuario']}, 200

                    else:

                        self.insert('usuarios',
                            [
                                "username",
                                "senha",
                                "status",
                                "user_admin",
                                "user_app",
                                "id_empresa"
                            ],
                            [
                                "'{}'".format(dados_dict['username']),
                                "'{}'".format(dados_dict['senha']),
                                "'{}'".format(dados_dict['status']),
                                "{}".format(dados_dict['user_admin']),
                                "{}".format(dados_dict['user_app']),
                                "{}".format(dados_dict['id_empresa'])
                            ]   
                        )

                        last_usuario_list = self.select('usuarios', ['id_usuario'], ['id_usuario=(select max(id_usuario) from usuarios)'])
                    
                        return {'Sucesso': 'Usuario cadastro com sucesso', 'id': last_usuario_list[0]['id_usuario']}, 200
                elif is_cliente:
                    return {"Error": "CPF já cadastrado"}, 400
                elif is_usuario:
                    return {"Error": "Usuário já cadastrado"}, 400
                    
        except Exception as e:
            print(e)
            return {"Error": "Parametros invalidos"}, 400