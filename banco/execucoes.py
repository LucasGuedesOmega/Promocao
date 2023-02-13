# -*- coding: UTF-8 -*-
from banco.conexao import Conecta
import datetime
import psycopg2

class Executa(Conecta):
    '''
        A classe Executa erda da classe conecta.
    '''
    def __init__(self):
        super().__init__()

        self.cursor = self.conectar()
      
    def select(self, table=str, fields_list=list, where_list=None, join_list=None, format_date=True, registro_unico=False):
        '''
            Constrói o select e executa o mesmo. 
        '''
        inicial_table = None

        if fields_list[0] == "*":
            fields_list.remove("*")

            self.cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' order by ordinal_position;".format(table))

            fields_db_list = self.cursor.fetchall()

            for field_tuple in fields_db_list:
                fields_list.append(field_tuple[0])
        
        if where_list and not join_list:

            query = 'SELECT {campos} from {tabela} where {condicao};'.format(campos = ','.join(fields_list), tabela = table, condicao = ' and '.join(where_list))

        elif where_list and join_list:
            
            inicial_table = table[0:2]

            query = 'SELECT {campos} from {tabela} {inicial_table} {join_table} where {condicao};'.format(
                campos = ','.join(fields_list), 
                tabela = table, 
                inicial_table=inicial_table,
                condicao = ' and '.join(where_list), 
                join_table = ''.join(join_list))

        elif join_list:
            inicial_table = table[0:2]
            
            query = 'SELECT {campos} from {tabela} {inicial_table} {join_table};'.format(  
                campos = ','.join(fields_list), 
                tabela = table, 
                inicial_table=inicial_table,
                join_table = ' '.join(join_list))

        else:
            query = 'SELECT {campos} from {tabela};'.format(campos = ','.join(fields_list), tabela = table)

        try:
            self.cursor.execute(query)
        except psycopg2.errors.InFailedSqlTransaction:
            self.cursor.execute("ROLLBACK")
            self.cursor.execute(query)

        fetch_list = self.cursor.fetchall()

        retorno_list = []

        for dados_list in fetch_list:
            retorno_dict = dict(zip(fields_list, dados_list))
       
            retorno_list.append(retorno_dict)

        arruma_key_list = []
      
        for retorno in retorno_list:
            
            key_list = retorno.keys()
            
            if format_date and table not in ['historico_table', 'voucher', 'venda']:
                for key in key_list:
                    if type(retorno[key]) == datetime.datetime:
                        retorno[key] = self.format_date(retorno[key])
                    if type(retorno[key]) == datetime.time:
                        retorno[key] = self.format_time(retorno[key])
            else:
                for key in key_list:
                    if type(retorno[key]) == datetime.datetime:
                        retorno[key] = self.format_date(retorno[key]) + " " + self.format_time(retorno[key])       
                    if type(retorno[key]) == datetime.time:
                        retorno[key] = self.format_time(retorno[key])

            arruma_key_dict = {}

            for key in key_list:
                if " as " in key:
                    key_separada = key.split(" as ")
                else:
                    key_separada = key.split(".")

                if len(key_separada) > 1:
                    arruma_key_dict[f"{key_separada[1]}"] = retorno[key]

            if arruma_key_dict:
                arruma_key_list.append(arruma_key_dict)

        if arruma_key_list:
            retorno_list = arruma_key_list
        
        if registro_unico and len(retorno_list) == 1:
            return retorno_list[0]

        return retorno_list

    def format_time(self, time):
        hora = time.hour

        if hora < 10:
            hora = "0" + f"{hora}"
        
        minuto = time.minute
        if minuto < 10:
            minuto = "0" + f"{minuto}"
        
        segundos = time.second
        if segundos < 10:
            segundos = "0" + f"{segundos}"
        
        return f"{hora}:{minuto}:{segundos}.000"

    def format_date(self, date):
        dia = date.day
        if date.day < 10:
            dia = "0" + f"{date.day}"

        mes = date.month
        if date.month < 10:
            mes = "0" + f"{date.month}"

        data = f"{date.year}-{mes}-{dia}"

        return data

    def insert(self, table=str, fields_list=list, values_list=list):
        '''
            Constrói e executa o insert.
        '''
        query = 'INSERT INTO {tabela} ({campos}) values ({valores});'.format(tabela=table, campos=','.join(fields_list), valores=','.join(values_list))

        try:
            self.cursor.execute(query)
            self.connection.commit()
        except psycopg2.errors.InFailedSqlTransaction:
            self.cursor.execute("ROLLBACK")
            self.connection.commit()
            self.cursor.execute(query)
            self.connection.commit()

    def update(self, table=str, set_list=list, where_list=None):
        if where_list:
            query = 'UPDATE {tabela} SET {set} WHERE {where};'.format(tabela=table, 
            set=', '.join(set_list), where=' and '.join(where_list))
        else:
            query = 'UPDATE {tabela} SET {set};'.format(table, set_list)

        try:
            self.cursor.execute(query)
            self.connection.commit()
        except psycopg2.errors.InFailedSqlTransaction:
            self.cursor.execute("ROLLBACK")
            self.connection.commit()
            self.cursor.execute(query)
            self.connection.commit()

    def delete(self, table=str, where_list=list):
        '''
            Constrói e executa o delete.
        '''
        query = 'DELETE FROM {tabela} WHERE {condicao};'.format(tabela=table, condicao=' and '.join(where_list))
        
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except psycopg2.errors.InFailedSqlTransaction:
            self.cursor.execute("ROLLBACK")
            self.connection.commit()
            self.cursor.execute(query)
            self.connection.commit()