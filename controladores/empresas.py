# -*- coding: UTF-8 -*-
from banco.execucoes import Executa
from geopy.geocoders import Nominatim

class Empresa(Executa):
    def __init__(self):
        super().__init__()
    
    def get_longitude_latidude(self, rua, numero, cidade, estado):
        endereco = f"{rua}, {numero}, {cidade}, {estado}"

        geolocator = Nominatim(user_agent='my_api')

        location = geolocator.geocode(endereco)

        if location:
            latitude = location.latitude
            longitude = location.longitude

            return latitude, longitude
        else:
            return None, None

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

                latitude, longitude = self.get_longitude_latidude(dados_dict['endereco'], dados_dict['numero'], dados_dict['cidade'], dados_dict['uf'])

                if empresa_list and latitude and longitude:
                    self.update('empresa',
                        [
                            "id_grupo_empresa={}".format(dados_dict['id_grupo_empresa']),
                            "razao_social='{}'".format(dados_dict['razao_social']),
                            "cep='{}'".format(dados_dict['cep']),
                            "cnpj='{}'".format(dados_dict['cnpj']),
                            "endereco='{}'".format(dados_dict['endereco']),
                            "numero={}".format(dados_dict['numero']),
                            "bairro='{}'".format(dados_dict['bairro']),
                            "uf='{}'".format(dados_dict['uf'].upper()),
                            "cidade='{}'".format(dados_dict['cidade']),
                            "status={}".format(dados_dict['status']),
                            "token_integracao='{}'".format(dados_dict['token_integracao']),
                            "latitude={}".format(latitude),
                            "longitude={}".format(longitude),
                        ],
                        ["id_empresa={}".format(dados_dict['id_empresa'])]
                    )
                elif latitude and longitude:
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
                            'cidade',
                            'status',
                            'token_integracao',
                            'latitude',
                            'longitude',
                        ],
                        [
                            "{}".format(dados_dict['id_grupo_empresa']),
                            "'{}'".format(dados_dict['razao_social']),
                            "'{}'".format(dados_dict['cep']),
                            "'{}'".format(dados_dict['cnpj']),
                            "'{}'".format(dados_dict['endereco']),
                            "{}".format(dados_dict['numero']),
                            "'{}'".format(dados_dict['bairro']),
                            "'{}'".format(dados_dict['uf'].upper()),
                            "'{}'".format(dados_dict['cidade'].upper()),
                            "{}".format(dados_dict['status']),
                            "'{}'".format(dados_dict['token_integracao']),  
                            "{}".format(latitude),  
                            "{}".format(longitude),  
                        ]
                    )
                elif not latitude and not longitude:
                    return {"error": "O Endereço informado está incorreto"}, 400

            return {"Sucesso": "Empresa inserida ou alterada com sucesso."}

        except Exception as e:
            print(e)
            return {"message": "Parametros iválidos"}, 400