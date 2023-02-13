# -*- coding: UTF-8 -*-
from banco.execucoes import Executa
import openpyxl

class Exportar(Executa):
    def __init__(self):
        super().__init__()

        self.caminho_excel = ".\\static\\arquivos_exportar\\exportar.xlsx"

        self.ex = openpyxl.load_workbook(self.caminho_excel)

    def exporta_excel(self, auth, dados_list):

        sheet = self.ex.worksheets[0]

        linha = 1

        sheet.delete_rows(1, sheet.max_row-1)

        for dados_dict in dados_list:
            colunas_list = dados_dict.keys()
            linha += 1

            for i, colunas in enumerate(colunas_list):
                sheet.cell(row=1, column=i+1).value = colunas
                sheet.cell(row=linha, column=i+1).value = dados_dict[colunas]
                
        self.ex.save(self.caminho_excel)

        return self.caminho_excel

        