# -*- coding: UTF-8 -*-
from banco.execucoes import Executa
import random
from datetime import datetime
from .venda import Venda
class Voucher(Executa):

    def __init__(self):
        super().__init__()

        self.venda_controller = Venda()

    def valida_codigo(self, dados_list, auth):

        lista_retorno = []
        
        for dados_dict in dados_list:
            voucher_list = self.select('voucher',
                [
                    '*'
                ],
                [
                    "codigo_voucher='{}'".format(dados_dict['codigoValidacao'])
                ],
                None,
                False
            )
            
            if voucher_list:
                voucher_dict = voucher_list[0]

                promocao_list = self.select('promocao', ['*'], [f"id_promocao={voucher_list[0]['id_promocao']}"], None, False)          
                produto_list = self.select('produtos', ['*'], [f"id_externo='{dados_dict['identificadorExternoProduto']}'"])

                promocao_dict = promocao_list[0]

                expira_voucher = self.compara_datas_voucher(voucher_dict)
                calculo_dict = self.calcula_desconto(dados_dict, promocao_dict)
                verifica_empresa = self.promocao_empresa(promocao_dict, dados_dict['codigoEmpresa'])
                verifica_datas = self.verifica_datas(promocao_dict)
                verifica_forma_pagamento = self.verifica_forma_pagamento(promocao_dict, dados_dict)

                if not expira_voucher and produto_list and verifica_empresa and verifica_datas and promocao_dict['status'] and verifica_forma_pagamento:
                    produto_dict = produto_list[0]

                    cliente_dict = self.select('clientes', ['*'], [f"id_usuario={auth['id_usuario']}"])[0]

                    self.insert_historico(dados_dict, calculo_dict, voucher_dict, cliente_dict)

                    placa = None
                    if dados_dict.get('placa'):
                        placa = dados_dict['placa']

                    if voucher_dict['tipocodigo'] == 'CASHBACK':
                        calculo_dict['desconto_unidade'] = 0
                        calculo_dict['desconto'] = 0

                    dict_retorno = {
                        "codigoValidacao": dados_dict['codigoValidacao'],
                        "valorPorUnidade": calculo_dict['valor_unidade'],
                        "valorPorUnidadeDesconto": calculo_dict['desconto_unidade'],
                        "valorDescontoTotal": calculo_dict['desconto'],
                        "valorVendaTotal": dados_dict['valorVenda'],
                        "quantidade": dados_dict['quantidade'],
                        "nomeCliente": cliente_dict['nome'],
                        "chaveAutenticacao": dados_dict['tokenIntegracao'],
                        "placa": placa,
                        "cpf": cliente_dict['cpf'],
                        "isAceitaCPF": True,
                        "isEmiteDocumentoFiscal": True,
                        "parametroOpcional": None,
                        "identificadorExternoProduto": dados_dict['identificadorExternoProduto'],
                        "tipoCodigo": voucher_list[0]['tipocodigo'],
                        "formaPagamento": dados_dict['descricaoFormaPagamento']
                    }

                    empresa_list = self.select('empresa', ['*'], [f"cnpj='{dados_dict['codigoEmpresa']}'"])
                    
                    if empresa_list:
                        dados_venda_list = [
                            {
                                'id_produto': produto_dict['id_produto'],
                                'valor': dados_dict['valorVenda'],
                                'valor_unidade': calculo_dict['valor_unidade'],
                                "desconto": calculo_dict['desconto'],
                                "desconto_unidade": calculo_dict['desconto_unidade'],
                                "quantidade": dados_dict['quantidade'],
                                "token_integracao": dados_dict['tokenIntegracao'],
                                "data_venda": dados_dict['dataVenda'],
                                "hora_venda": dados_dict['horaVenda'],
                                "id_forma_pagamento": 'null',
                                "contigencia": False,
                                "id_promocao": promocao_dict['id_promocao'],
                                "id_empresa": empresa_list[0]['id_empresa'],
                                "id_usuario": auth['id_usuario'],
                                "status_venda": "EMITIDA",
                                "descricao_forma_pagamento": dados_dict['descricaoFormaPagamento'],
                                'link_documento_fiscal': 'null'
                            }
                        ]

                        self.venda_controller.insert_or_update(dados_venda_list)
                        self.update('voucher', ["usado=true"], [f"id_voucher={voucher_dict['id_voucher']}"])

                        lista_retorno.append(dict_retorno)

                elif expira_voucher:
                    return {'erros': ['Voucher Expirado ou ja usado anteriormente.']}, 400
                elif not produto_list:
                    return {'erros': ['O produto selecionado para venda nao e o mesmo do voucher.']}, 400
                elif not verifica_empresa:
                    return {'erros': ['Empresa nao esta na promocao.']}, 400
                elif not verifica_datas:
                    return {'erros': ['A promocao ja expirou ou nao esta em um dia da semana valido.']}, 400
                elif not promocao_dict['status']:
                    return {'erros': ['A promocao nao esta ativa.']}, 400 
                elif not verifica_forma_pagamento:
                    return {'erros': ['A forma de pagamento nao esta na promocao.']}, 400 
            else:
                return {'erros': ['Voucher incorreto.']}, 400

        return lista_retorno

    def insert_historico(self, dados_dict, calculo_dict, voucher_dict, cliente_dict):
        data_emissao = f"{dados_dict['dataVenda']} {dados_dict['horaVenda']}" 

        if cliente_dict and calculo_dict['desconto'] > 0:
            self.insert('historico_promocao', ['id_cliente', 'valor_total_venda','valor', 'data_emissao', 'tipo'], [str(cliente_dict['id_cliente']), str(dados_dict['valorVenda']), str(calculo_dict['desconto']), f"'{data_emissao}'", f"'{voucher_dict['tipocodigo']}'"])

            where_total = [f"id_cliente={cliente_dict['id_cliente']}", f"tipo='{voucher_dict['tipocodigo']}'"]

            total_cliente_list = self.select("total_valores_clientes", ['*'], where_total)

            if total_cliente_list:
                soma_desconto = total_cliente_list[0]['valor'] + calculo_dict['desconto']
                self.update("total_valores_clientes", [f"valor={str(soma_desconto)}"], where_total)
            else:
                self.insert("total_valores_clientes", ["id_cliente", 'valor', 'tipo'], [str(cliente_dict['id_cliente']), str(calculo_dict['desconto']), f"'{voucher_dict['tipocodigo']}'"])

    def verifica_forma_pagamento(self, promocao, dados_dict):
        formas_pagamento_list = self.select('grupo_forma_pagamento',
            ['fp.id_externo'],
            [f"gr.id_grupo_pagamento={promocao['id_grupo_pagamento']}"],
            ["left join forma_pagamento fp on (fp.id_forma_pagamento=gr.id_forma_pagamento)"]
        )
        
        list_id_externos = []
        for formas_pagamento_dict in formas_pagamento_list:
            list_id_externos.append(formas_pagamento_dict['fp.id_externo'])
        
        if dados_dict['identificadorExternoFormaPagamento'] in list_id_externos:
            return True
        
        return False

    def verifica_datas(self, promocao_dict):
        
        hoje = datetime.now()
        data_final_promocao = promocao_dict['data_fim']
        semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']

        if hoje > data_final_promocao:
            return False

        if not promocao_dict[semana[hoje.weekday()]]:
            return False

        return True

    def promocao_empresa(self, promocao, cnpj_dados_autosystem):
        promocao_empresas_list = self.select('promocao_empresas', ['*'], [f"id_promocao={promocao['id_promocao']}"])

        for promocao_empresas_dict in promocao_empresas_list:
            empresa_dict = self.select('empresa', ['*'], [f"id_empresa={promocao_empresas_dict['id_empresa']}"])[0]

            if empresa_dict['cnpj'] == cnpj_dados_autosystem:
                return True

        return False

    def compara_datas_voucher(self, voucher_dict):
        data_ini_db = voucher_dict['data_ini']
        agora = datetime.now()

        diferenca = agora - data_ini_db
        
        if diferenca.seconds < 900 and not voucher_dict['usado']:
            return False
        elif voucher_dict['usado']:
            return True

    def calcula_desconto(self, dados_autosystem, dados_promocao):
        valor_unidade = round((dados_autosystem['valorVenda'] / dados_autosystem['quantidade']), 3)
        desconto = 0
        desconto_unidade = dados_promocao['desconto_por_unidade']

        if dados_autosystem['quantidade'] > dados_promocao['quantidade'] and dados_promocao['tipo'] == 1:

            desconto = dados_autosystem['quantidade'] * dados_promocao['desconto_por_unidade']

        elif dados_autosystem['quantidade'] > dados_promocao['quantidade'] and dados_promocao['tipo'] == 2:
            
            desconto_unidade = valor_unidade * dados_promocao['desconto_por_unidade'] / 100

            desconto = dados_autosystem['quantidade'] * desconto_unidade

        retorno_dict = {
            'valor_unidade': valor_unidade,
            'desconto': round(desconto, 2),
            'desconto_unidade': round(desconto_unidade, 2),
        }

        return retorno_dict

    def insert_ou_update(self, dados_dict, auth):
        try:
            codigo_voucher = random.randint(11111, 999999)
 
            voucher_list = self.select('voucher', 
                ['id_voucher'],
                ['id_usuario={}'.format(auth['id_usuario'])]
            )

            data_ini = datetime.now()

            if dados_dict['usado'] == False:
                dados_dict['usado'] = 'false'
            else: 
                dados_dict['usado'] = 'true'

            if voucher_list:
                self.update('voucher', 
                    [
                        "codigo_voucher='{}'".format(codigo_voucher), "data_ini='{}'".format(data_ini),
                        "id_promocao={}".format(dados_dict['id_promocao']),"status='{}'".format(dados_dict['status']),
                        "id_empresa={}".format(dados_dict['id_empresa']), "id_usuario={}".format(auth['id_usuario']),
                        "tipoCodigo='{}'".format(dados_dict['tipoCodigo']), "usado={}".format(dados_dict['usado'])
                    ],
                    ["id_voucher={}".format(voucher_list[0]['id_voucher'])]
                )
            
            else:
                self.insert('voucher',
                    [
                        "codigo_voucher",
                        "id_usuario",
                        "data_ini",
                        "id_promocao",
                        "id_empresa",
                        "tipoCodigo",
                        "status",
                        "usado",
                    ],
                    [
                        "'{}'".format(codigo_voucher),
                        "{}".format(auth['id_usuario']),
                        "'{}'".format(data_ini),
                        "{}".format(dados_dict['id_promocao']),
                        "{}".format(dados_dict['id_empresa']),
                        "'{}'".format(dados_dict['tipoCodigo']),
                        "{}".format(dados_dict['status']),
                        "{}".format(dados_dict['usado']),
                    ]
                )

            return {"Voucher": codigo_voucher}

        except Exception as e:
            print(e)
            return {"Error": "Parametros invalidos."}