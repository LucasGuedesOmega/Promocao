# -*- coding: UTF-8 -*-
import psycopg2 as db
from psycopg2.extras import DictCursor
class Conecta:
    '''
        Classe de conexão com banco de dados
    '''
    def __init__(self):

        self.host = 'localhost'
        self.database = 'dbpromocao'
        self.user = 'postgres'
        self.senha = 'postgres'
        self.port = '5433'

    def conectar(self):

        self.connection = db.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.senha,
            port=self.port
        )

        self.cursor = self.connection.cursor(cursor_factory=DictCursor)

        return self.cursor