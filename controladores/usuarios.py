from banco.execucoes import Executa

class Usuario(Executa):
    def __init__(self):
        super().__init__()

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
                            "e_mail='{}'".format(dados_dict['e_mail']),
                            "status={}".format(dados_dict['status']),
                            "user_admin={}".format(dados_dict['user_admin']),
                            "id_empresa={}".format(dados_dict['id_empresa']),
                            "nome='{}'".format(dados_dict['nome']),
                            "cpf_cnpj='{}'".format(dados_dict['cpf_cnpj']),
                        ],
                        where_list  
                    )
                
                else:

                    self.insert('usuarios',
                        [
                            "username",
                            "senha",
                            "e_mail",
                            "status",
                            "user_admin",
                            "id_empresa",
                            'nome',
                            'cpf_cnpj'
                        ],
                        [
                            "'{}'".format(dados_dict['username']),
                            "'{}'".format(dados_dict['senha']),
                            "'{}'".format(dados_dict['e_mail']),
                            "'{}'".format(dados_dict['status']),
                            "{}".format(dados_dict['user_admin']),
                            "{}".format(dados_dict['id_empresa']),
                            "'{}'".format(dados_dict['nome']),
                            "'{}'".format(dados_dict['cpf_cnpj']),
                        ]   
                    )

            return {"Sucesso": "Usuário cadastrado com sucesso!"}, 200

        except Exception as e:
            print(e)
            return {"Error": "Parametros invalidos"}, 400