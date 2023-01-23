# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class GrupoFormaPagamento(Executa):
    def __init__(self):
        super().__init__()

    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list:
                grupo_forma_pagamento_list = None
                if dados_dict.get('id_grupo_forma_pagamento'):
                    grupo_forma_pagamento_list = self.select('grupo_forma_pagamento', 
                        [
                            '*'
                        ],
                        [ "id_grupo_forma_pagamento={}".format(dados_dict['id_grupo_forma_pagamento'])]
                    )
                
                if grupo_forma_pagamento_list:

                    self.update("grupo_forma_pagamento", 
                        [
                            "id_grupo_pagamento={}".format(dados_dict['id_grupo_pagamento']),
                            "id_forma_pagamento={}".format(dados_dict['id_forma_pagamento'])
                        ],
                        [ "id_grupo_forma_pagamento={}".format(dados_dict['id_grupo_forma_pagamento'])]
                    )
                else:
                    self.insert('grupo_forma_pagamento',
                        [
                            "id_grupo_pagamento",
                            "id_forma_pagamento",
                            'id_empresa',
                            'id_grupo_empresa',
                        ],
                        [
                            "{}".format(dados_dict['id_grupo_pagamento']), 
                            "{}".format(dados_dict['id_forma_pagamento']), 
                            "{}".format(dados_dict['id_empresa']), 
                            "{}".format(dados_dict['id_grupo_empresa']), 
                        ]
                    )

            return {"Sucesso": "Grupo de forma de pagamento inserido ou alterado com sucesso."}, 200

        except Exception as e:
            print(e)
            return {"Error": f"Parametros inválidos {e}."}, 400