import json
import time
import argparse
import requests
import random
from pprint import pprint
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

VOTANTES_FILE = './wallets.json'
URL_SERVER = 'http://localhost:5000'


def send_voto(votante, centros, candidatosPresidente, candidatosGobernador, count):

    address = votante.get('address')
    localidad = votante.get('localidad')
    centro = votante.get('centro')
    candidatoPresi = random.choice(candidatosPresidente)
    candidatoGob = random.choice(candidatosGobernador.get(localidad))
    
    # body del votante
    body = {
        'address': address,
        'localidad': localidad,
        'presidente': candidatoPresi,
        'gobernador': candidatoGob
    }

    # url = ''
    url = f"{centros[0]}:{centros[1]}/api/votar/"
    # Buscar la url del centro
    # for i in centros:
    #     if centros[0][-1] == centro:
    #         url = f"{centros[0]}:{centros[1]}/api/votar/"
    
    # Enviar la peticion
    response = requests.post(url, data=body)

    print(response)


def test():
    time.sleep(1)
    print("AAAAAAAAA")

class GeneradorVotos():

    def __init__(self, file, concurrency):
        self.concurrency = int(concurrency)

        # Leer Json de Votantes
        v_file = open(VOTANTES_FILE, 'r')
        self.votantes = json.loads(v_file.read())
        self.centros = []

        # Ordenamos los candidatos
        self.candidatosPresidencia = [None] # Inicializar con None para el caso de voto blanco
        self.candidatosGobernador = {}

        for votante in self.votantes.values():
            if int(votante.get('candidato')) == 1:
                self.candidatosPresidencia.append(votante)
            elif int(votante.get('candidato')) == 2:
                localidad = votante.get('localidad')
                aux = self.candidatosGobernador.get(localidad)
                if not aux:
                    self.candidatosGobernador[localidad] = [None] # Inicializar con None para el caso de voto blanco
                self.candidatosGobernador[localidad].append(votante)


        # Leer archivos 
        with open(file, 'r') as fd:
            n_centros = fd.readline()
            for i in range(int(n_centros)):
                self.centros.append(fd.readline().rstrip().split(' '))

        # pprint(self.votantes)
        # pprint(self.centros)
        # print(self.candidatosPresidencia)
        # print(self.candidatosGobernador)

    def run(self):
        """
        Funcion para ejecutar los votos al servidor
        """
        print(self.concurrency, type(self.concurrency))
        pool = ThreadPoolExecutor(self.concurrency)
        print("Empezando Pool")

        pool.submit(test)

        pool.submit(
            send_voto,
            votante = list(self.votantes.values())[0],
            centros = self.centros,
            candidatosPresidencia = self.candidatosPresidencia,
            candidatosGobernador = self.candidatosGobernador,
            count = 0
        )
        # for count, votante in enumerate(self.votantes.values()):
        #     print(count)


        print("Listo")


if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some file.')
    parser.add_argument('-n', type=str, help='Archivo de Centros de Votacion')
    parser.add_argument('-nc', type=str, help="Numero de concurrencia")
    args = parser.parse_args()

    generator = GeneradorVotos(args.n, args.nc)
    generator.run()