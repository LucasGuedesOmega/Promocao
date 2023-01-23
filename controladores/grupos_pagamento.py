# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class GrupoPagamento(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):

        try:
            for dados_dict in dados_list:

                if dados_dict['id_grupo_pagamento'] is None:
                    grupo_pagamento_list = None
                else:
                    grupo_pagamento_list = self.select('grupo_pagamento',
                        [
                            "id_grupo_pagamento"
                        ],
                        [
                            "id_grupo_pagamento={}".format(dados_dict['id_grupo_pagamento'])
                        ]
                    )

                if grupo_pagamento_list:
                    self.update('grupo_pagamento',
                        [
                            "descricao='{}'".format(dados_dict['descricao']), 
                            "status={}".format(dados_dict['status'])
                        ],
                        [
                            "id_grupo_pagamento={}".format(dados_dict['id_grupo_pagamento'])
                        ]
                    )
                else:
                    self.insert('grupo_pagamento',
                        [
                            "descricao", 
                            "status", 
                            "id_empresa",
                            "id_grupo_empresa",
                        ],
                        [
                            "'{}'".format(dados_dict['descricao']), 
                            "{}".format(dados_dict['status']),
                            "{}".format(dados_dict['id_empresa']), 
                            "{}".format(dados_dict['id_grupo_empresa']), 
                        ]
                    )

            return {"Sucesso": "Grupo de pagamento inserido ou alterado com sucesso."}, 200

        except Exception as e:

            return {"Error": f"Parametros inválidos {e}."}, 400