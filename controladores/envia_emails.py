# -*- coding: UTF-8 -*-
from banco.execucoes import Executa
from flask_mail import Message
import jinja2
import random
import datetime

class EnviaEmail(Executa):
    def __init__(self, mail):
        super().__init__()
    
        self.mail = mail
    
    def envia_email(self, dados_list):
        for dados_dict in dados_list:

            if dados_dict.get("tipo_email") and dados_dict['tipo_email'] == 'confirmacao_email' and dados_dict.get('nome') and dados_dict.get('destinatario') and dados_dict.get('id_usuario'):
                return self.confirmacao_email(dados_dict['nome'], dados_dict['destinatario'], dados_dict['id_usuario'])

    def confirmacao_email(self, nome, destinatario, id_usuario):
        msg = Message('Verificar E-mail', sender='lucas_guidolinguedes@outlook.com', recipients=[destinatario])

        html = open("controladores/email/confirma_cadastro.html", 'r', encoding='UTF-8')
        text = html.read()
        
        format_text = jinja2.Template(text)

        codigo = random.randint(000000, 999999)

        msg.html = format_text.render().format(name=nome, codigo=codigo)
    
        self.mail.send(msg)

        data = self.format_date(datetime.datetime.now()) + " " + self.format_time(datetime.datetime.now())

        self.insert('confirma_email', ['id_usuario', 'codigo', 'data'], [f"{id_usuario}", f"'{codigo}'", f"'{data}'"])

        return {'sucesso': 'enviado email com sucesso.'}, 200
    
    def confirmacao_codigo(self, dados_dict):
        if dados_dict.get('codigo'):
            confirma_dict = self.select('confirma_email', ['*'], [f"codigo='{dados_dict['codigo']}'"], registro_unico=True)
            if confirma_dict:
                self.delete('confirma_email', [f"id_usuario={confirma_dict['id_usuario']}"])

                return {'Sucesso': 'E-mail confirmado com sucesso.'}, 200
        else:
            return {'Error': 'Por favor fornaça o codigo de confirmação.'}, 400