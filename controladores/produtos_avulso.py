# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class ProdutoAvulso(Executa):
    def __init__(self):
        super().__init__()
    
    def insert_ou_update(self, dados_list):
        
        try:
            for dados_dict in dados_list:
                
                if dados_dict['id_produto_avulso'] is None:
                    produto_avulso_list = None
                else: 
                    produto_avulso_list = self.select('produto_avulso', 
                        [
                            "*"
                        ],
                        [
                            "id_produto_avulso={}".format(dados_dict['id_produto_avulso'])
                        ]
                    )
                
                if produto_avulso_list:
                    self.update('produto_avulso',
                        [
                            "id_produto={}".format(dados_dict['id_produto']),
                            "id_grupo_empresa={}".format(dados_dict['id_grupo_empresa']),
                            "id_empresa={}".format(dados_dict['id_empresa']),
                            "id_grupo_pagamento={}".format(dados_dict['id_grupo_pagamento']),
                            "valor_desconto={}".format(dados_dict['valor_desconto']),
                            "valor_cash_back={}".format(dados_dict['valor_cash_back']),
                        ],
                        [
                            "id_produto_avulso={}".format(dados_dict['id_produto_avulso'])
                        ]
                    )
                else:
                    self.insert('produto_avulso', 
                        [
                            'id_produto',
                            'id_grupo_empresa',
                            'id_empresa',
                            'id_grupo_pagamento',
                            'valor_desconto',
                            'valor_cash_back',
                            'id_empresa',
                        ],               
                        [
                            "{}".format(dados_dict['id_produto']),
                            "{}".format(dados_dict['id_grupo_empresa']),
                            "{}".format(dados_dict['id_empresa']),
                            "{}".format(dados_dict['id_grupo_pagamento']),
                            "{}".format(dados_dict['valor_desconto']),
                            "{}".format(dados_dict['valor_cash_back']),
                            "{}".format(dados_dict['id_empresa']),
                        ]
                    )      

            return {"Sucesso": "Produto Avulso inserido ou alterado com sucesso."}

        except KeyError:
            
            return {"Error": "Parametros inválidos."}