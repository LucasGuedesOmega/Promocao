from banco.execucoes import Executa

class Empresa(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list:
                
                dados_dict['cep'] = ''.join(char for char in dados_dict['cep'] if char.isalnum())
                dados_dict['cnpj'] = ''.join(char for char in dados_dict['cnpj'] if char.isalnum())

                if dados_dict['id_empresa'] is None:
                    empresa_list = None
                else:
                    empresa_list = self.select('empresa',
                        ['id_empresa'],
                        ["id_empresa={}".format(dados_dict['id_empresa'])]
                    )

                if empresa_list:
                    self.update('empresa',
                        [
                            "id_grupo_empresa={}".format(dados_dict['id_grupo_empresa']),
                            "razao_social='{}'".format(dados_dict['razao_social']),
                            "cep='{}'".format(dados_dict['cep']),
                            "cnpj='{}'".format(dados_dict['cnpj']),
                            "endereco='{}'".format(dados_dict['endereco']),
                            "numero={}".format(dados_dict['numero']),
                            "bairro='{}'".format(dados_dict['bairro']),
                            "uf='{}'".format(dados_dict['uf']),
                            "status={}".format(dados_dict['status']),
                            "token_integracao='{}'".format(dados_dict['token_integracao']),
                        ],
                        ["id_empresa={}".format(dados_dict['id_empresa'])]
                    )
                else:
                    self.insert('empresa', 
                        [
                            "id_grupo_empresa",
                            'razao_social',
                            'cep',
                            'cnpj',
                            'endereco',
                            'numero',
                            'bairro',
                            'uf',
                            'status',
                            'token_integracao',
                        ],
                        [
                            "{}".format(dados_dict['id_grupo_empresa']),
                            "'{}'".format(dados_dict['razao_social']),
                            "'{}'".format(dados_dict['cep']),
                            "'{}'".format(dados_dict['cnpj']),
                            "'{}'".format(dados_dict['endereco']),
                            "{}".format(dados_dict['numero']),
                            "'{}'".format(dados_dict['bairro']),
                            "'{}'".format(dados_dict['uf']),
                            "{}".format(dados_dict['status']),
                            "'{}'".format(dados_dict['token_integracao']),  
                        ]
                    )

            return {"Sucesso": "Empresa inserida ou alterada com sucesso."}

        except Exception as e:
            print(e)
            return {"message": "Parametros iválidos"}, 400