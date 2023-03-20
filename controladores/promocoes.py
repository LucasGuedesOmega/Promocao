# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class Promocao(Executa):
    def __init__(self):
        super().__init__()

    def insert_ou_update(self, dados_list):
       
        for dados_dict in dados_list:
            
            keys_list = dados_dict.keys()

            obrigatorios_list = ['titulo', 'tipo', 'desconto_total', 'desconto_por_unidade', 'id_produto', 'id_grupo_empresa', 'id_grupo_empresa', 
                                'data_ini', 'data_fim']

            for key in keys_list:
                if dados_dict[key] == None:
                    if key in obrigatorios_list:
                        return { 'Error': f'O campo {key} é obrigatório' }, 400
                    else:
                        dados_dict[key] = 'null'

            if dados_dict['id_promocao'] is None:
                promocao_list = None
            else:
                promocao_list = self.select('promocao',
                    [ 'id_promocao' ],
                    ["id_promocao={}".format(dados_dict['id_promocao']), "id_grupo_empresa={}".format(dados_dict['id_grupo_empresa'])]
                )

            if promocao_list:   
                
                self.update('promocao',
                    [
                        "titulo='{}'".format(dados_dict['titulo']), "tipo='{}'".format(dados_dict['tipo']),
                        "desconto_total={}".format(dados_dict['desconto_total']),"desconto_por_unidade={}".format(dados_dict['desconto_por_unidade']),
                        "id_produto={}".format(dados_dict['id_produto']), "id_grupo_empresa={}".format(dados_dict['id_grupo_empresa']),
                        "data_ini='{}'".format(dados_dict['data_ini']), "data_fim='{}'".format(dados_dict['data_fim']), "imagem='{}'".format(dados_dict['imagem']),
                        "segunda={}".format(dados_dict['segunda']), "terca={}".format(dados_dict['terca']), "quarta={}".format(dados_dict['quarta']), 
                        "quinta={}".format(dados_dict['quinta']), "sexta={}".format(dados_dict['sexta']), "sabado={}".format(dados_dict['sabado']),
                        "domingo={}".format(dados_dict['domingo']), "status={}".format(dados_dict['status']), "id_grupo_pagamento={}".format(dados_dict['id_grupo_pagamento']),
                        "quantidade={}".format(dados_dict['quantidade'])
                    ],
                    [
                        "id_promocao={}".format(dados_dict['id_promocao'])
                    ]
                )

                return {'Sucesso': 'Promoções cadastradas ou alteradas com sucesso!', 'id': dados_dict['id_promocao']}, 200
            else:
                
                self.insert('promocao',
                    [
                        'titulo', 'tipo', 'desconto_total', 'desconto_por_unidade', 'id_produto', 'id_grupo_empresa', 'data_ini', 'data_fim',
                        'imagem', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo', 'status', 'id_grupo_pagamento', 'quantidade'
                    ],
                    [
                        "'{}'".format(dados_dict['titulo']), "'{}'".format(dados_dict['tipo']), "{}".format(dados_dict['desconto_total']),
                        "{}".format(dados_dict['desconto_por_unidade']), "{}".format(dados_dict['id_produto']), "{}".format(dados_dict['id_grupo_empresa']),
                        "'{}'".format(dados_dict['data_ini']), "'{}'".format(dados_dict['data_fim']),
                        "'{}'".format(dados_dict['imagem']), "{}".format(dados_dict['segunda']), "{}".format(dados_dict['terca']), "{}".format(dados_dict['quarta']), 
                        "{}".format(dados_dict['quinta']), "{}".format(dados_dict['sexta']), "{}".format(dados_dict['sabado']), "{}".format(dados_dict['domingo']), 
                        "{}".format(dados_dict['status']), "{}".format(dados_dict['id_grupo_pagamento']), "{}".format(dados_dict['quantidade'])
                    ]
                )

                last_promocao_dict = self.select('promocao', ['id_promocao'], ['id_promocao=(select max(id_promocao) from promocao)'], registro_unico=True)
                
                return {'Sucesso': 'Promoções cadastradas ou alteradas com sucesso!', 'id': last_promocao_dict['id_promocao']}, 200


