# -*- coding: UTF-8 -*-
from banco.execucoes import Executa

class Busca(Executa):
    def __init__(self):
        super().__init__()

    def buscar(self, parametros_dict, auth, table=str):

        try:
            
            if auth.get('id_usuario'):

                chave_list = list(parametros_dict.keys())
                valor_list = list(parametros_dict.values())

                where_list = []
                campos_list = None

                if chave_list and valor_list:
                    for num, chave_dict in enumerate(chave_list):
                        
                        if " and " in valor_list[num]:
                            dates_list = valor_list[num].split(' and ')           
                            where = "{} BETWEEN '{}' AND '{}'".format(chave_dict, dates_list[0], dates_list[1])
                        elif ">" in valor_list[num] and "=" not in valor_list[num]:
                            valor_list[num] = ''.join( x for x in valor_list[num] if x not in ">")
                            where = "{}>'{}'".format(chave_dict, valor_list[num])

                        elif "<" in valor_list[num] and "=" not in valor_list[num] :
                            valor_list[num] = ''.join( x for x in valor_list[num] if x not in "<")
                            where = "{}<'{}'".format(chave_dict, valor_list[num])
                        elif ">=" in valor_list[num]:
                            valor_list[num] = ''.join( x for x in valor_list[num] if x not in ">=")
                            where = "{}>='{}'".format(chave_dict, valor_list[num])
                        elif "<=" in valor_list[num]:
                            valor_list[num] = ''.join( x for x in valor_list[num] if x not in "<=")
                            where = "{}<='{}'".format(chave_dict, valor_list[num])
                        elif "!=" in valor_list[num]:
                            valor_list[num] = ''.join( x for x in valor_list[num] if x not in "!=")
                            where = "{}!='{}'".format(chave_dict, valor_list[num])
                            if valor_list[num] == 'true' or valor_list[num] == 'false':
                                where = "{}!={}".format(chave_dict, valor_list[num])

                        elif chave_dict != "campos":
                            where = "{}='{}'".format(chave_dict, valor_list[num])
                            if valor_list[num] == 'true' or valor_list[num] == 'false':
                                where = "{}={}".format(chave_dict, valor_list[num])

                        if chave_dict == "campos":
                            campos_list = valor_list[num].split(', ')

                        where_list.append(where)

                usuario_list = self.select('usuarios', ['id_empresa'], [f"id_usuario={auth['id_usuario']}"])

                if table != 'empresa' and table != 'grupo_empresa' and table != 'usuarios' and table != 'promocao_empresas':
                    for usuario_dict in usuario_list :
                        where_list.append(f"id_empresa={usuario_dict['id_empresa']}")
            
                if campos_list:
                    promocao_item_list = self.select(table,
                        campos_list,
                        where_list
                    )
                else:
                    promocao_item_list = self.select(table,
                        [
                            "*"
                        ],
                        where_list
                    )

                return promocao_item_list            

            else:
                return {'Error': "Favor refazer login!"}, 400

        except KeyError:
            return {"Error": "Parametros inválidos"}, 400