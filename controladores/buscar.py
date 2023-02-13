# -*- coding: UTF-8 -*-
from banco.execucoes import Executa
import psycopg2

class Busca(Executa):
    def __init__(self):
        super().__init__()

    def parametros(self, chave_list, valor_list):
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
                
        return where_list, campos_list

    def buscar(self, parametros_dict, auth, table=str):

        try:
            if auth.get('id_usuario'):
                chave_list = list(parametros_dict.keys())
                valor_list = list(parametros_dict.values())

                where_list = self.parametros(chave_list, valor_list)[0]
                campos_list = self.parametros(chave_list, valor_list)[1]

                usuario_dict = self.select('usuarios', ['*'], [f"id_usuario={auth['id_usuario']}"], registro_unico=True)
            
                if table != 'empresa' and table != 'grupo_empresa' and table != 'usuarios' and table != 'promocao_empresas' and table != 'tela_acao' and table != 'permissao_tela_acao':
                    where_list.append(f"id_grupo_empresa={usuario_dict['id_grupo_empresa']}")

                try:
                    if campos_list:
                        retorno_item_list = self.select(table,
                            campos_list,
                            where_list,
                            format_date=True
                        )
                    else:
                        retorno_item_list = self.select(table,
                            [
                                "*"
                            ],
                            where_list,
                            format_date=True
                        )
                
                    if retorno_item_list and table != 'tela_acao' and table != 'permissao_tela_acao' and not auth['user_admin'] and auth['id_grupo_empresa'] != retorno_item_list[0]['id_grupo_empresa']:
                        return {'error': 'Você não tem permissão'}, 400

                    return retorno_item_list            

                except psycopg2.errors.UndefinedColumn:
                    if usuario_dict['user_admin']:
                        return {'LOG': 'Admin encontrado'}, 200

                except psycopg2.errors.InvalidTextRepresentation:
                    if usuario_dict['user_admin']:
                        return {'LOG': 'Admin encontrado'}, 200

                except Exception as e:
                    return {"Error": e}, 400
            else:
                return {'Error': "Favor refazer login!"}, 400

        except KeyError:
            return {"Error": "Parametros inválidos"}, 400