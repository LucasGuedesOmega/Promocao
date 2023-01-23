# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class FormaPagamento(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list:
                if dados_dict['id_forma_pagamento'] is None:
                    forma_pagamento_list = None
                else:
                    forma_pagamento_list = self.select('forma_pagamento', 
                        [
                            '*'
                        ],
                        [
                            'id_forma_pagamento={}'.format(dados_dict['id_forma_pagamento'])
                        ]
                    )
                
                if forma_pagamento_list:
                    self.update('forma_pagamento',
                        [
                            "status={}".format(dados_dict['status']),
                            "tipo='{}'".format(dados_dict['tipo']),
                            "id_externo={}".format(dados_dict['id_externo']),
                            "descricao='{}'".format(dados_dict['descricao']),
                        ],
                        [
                            "id_forma_pagamento={}".format(dados_dict['id_forma_pagamento'])
                        ]
                    )
                    
                    return {"Sucesso": "Forma de pagamento inserida ou alterada com sucesso.", 'id': dados_dict['id_forma_pagamento']}, 200

                else:
                    self.insert('forma_pagamento',
                        [
                            "status",
                            "tipo",
                            "id_externo",
                            "descricao",
                            "id_empresa",
                            "id_grupo_empresa",
                        ],
                        [
                            "{}".format(dados_dict['status']),
                            "'{}'".format(dados_dict['tipo']),
                            "{}".format(dados_dict['id_externo']),
                            "'{}'".format(dados_dict['descricao']),
                            "{}".format(dados_dict['id_empresa']),
                            "{}".format(dados_dict['id_grupo_empresa']),
                        ]
                    )

                    last_forma_pagamento = self.select('forma_pagamento', ['id_forma_pagamento'], ['id_forma_pagamento=(select max(id_forma_pagamento) from forma_pagamento)'], registro_unico=True)

                    return {"Sucesso": "Forma de pagamento inserida ou alterada com sucesso.", 'id': last_forma_pagamento['id_forma_pagamento']}, 200

        except Exception as e:
            
            return {"Error": f"Parametros inválidos {e}."}, 400