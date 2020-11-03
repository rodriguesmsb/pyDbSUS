#!/usr/bin/env python3

from sys import argv
from os import path, listdir, system
from dbfread import DBF
import pandas as pd

folder = path.dirname(__file__)
blast_dbf = path.join(folder, 'blast_dbf')


class ReadDbf:
    """Converte o arquivo database inserido de acordo com o
    fluxograma  [+] dbc -> dbf -> csv [+]
    """

    def __init__(self, file_dbf, convert='convert'):
        """A instancia recebe um parametro o nome do arquivo dbf
        e abre uma lista para os itens que serão iterados no dbf
        """
        self.file_dbf = file_dbf

        if convert == 'convert':
            if path.isfile(self.file_dbf):
                self.read_dbf_to_csv(
                    self.__check_file_dbf(file_dbf))

        else:
            ...

    def __check_file_dbf(self, file_dbf):
        """Confere se o arquivo inserido está no formato dbf
        se estiver, o arquivo será convertido diretamente para csv,
        caso contrário o mesmo irá passar pela conversão para dbf
        através da ferramenta blast-dbf que se encontra no mesmo
        diretório deste script
        """
        if bool(file_dbf.endswith(('.dbf', '.DBF'))):
            return file_dbf

        elif bool(file_dbf.endswith(('.dbc', '.DBC'))):
            system(f"./blast-dbf {file_dbf} {file_dbf.split('.')[0]}.dbf")
            return file_dbf.split('.')[0] + '.dbf'

        else:
            print(f'O arquivo {file_dbf} não é válido')

    def to_dataframe(self):
        dataframe = {}

        for key in DBF(file_dbf, encoding='ISO-8859-1',
                       load=True).field_names:
            dataframe[key] = []

        for line in range(0, len(DBF(file_dbf,
                          encoding='ISO-8859-1', load=True))):

            for n_value in DBF(file_dbf, encoding='ISO-8859-1',
                               load=True).records[line].values():
                for n_key in dataframe.keys():
                    dataframe[n_key].append(n_value)

        print('to_dataframe')
        return dd.from_pandas(pd.DataFrame(dataframe), npartitions=2)

    def read_dbf_to_csv(self, file_dbf):
        """Abre um arquivo com o nome do dbf splitado e substituindo a
        extensão .dbf por .csv. Depois é escrito o cabeçalho utilizando
        os campos tidos como fields_names pelo dbf, para posteriormente
        serem gravados como cabeçalho do arquivo csv.
        Aplica um loop para iterar os valores de dicionários dentro do
        arquivo dbf diretamente no arquivo csv.
        """
        df = {}
        db = DBF(file_dbf, encoding='iso-8859-1', load=True)

        for column in db.field_names:
            df[column] = []

        for i in range(0, len(db)):
            for column, value in zip(db.field_names, db.records[i].values()):
                df[column].append(value)

        print('read_dbf_to_csv')
        pd.DataFrame(df).to_csv('{}.csv'.format(file_dbf.split('.')[0]))


if __name__ == '__main__':
    ReadDbf(file_dbf=argv[1], convert=argv[2])
