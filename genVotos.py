import json
import time
import argparse
import requests
import random
from concurrent.futures import ThreadPoolExecutor

VOTANTES_FILE = './wallets.json'
URL_SERVER = 'http://localhost:5000'

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
                self.candidatosPresidencia.append(votante['address'])
            elif int(votante.get('candidato')) == 2:
                localidad = votante.get('location')
                aux = self.candidatosGobernador.get(localidad)
                if not aux:
                    self.candidatosGobernador[localidad] = [None] # Inicializar con None para el caso de voto blanco
                self.candidatosGobernador[localidad].append(votante['address'])


        # Leer archivos 
        with open(file, 'r') as fd:
            n_centros = fd.readline()
            for i in range(int(n_centros)):
                self.centros.append(fd.readline().rstrip().split(' '))

        print(self.candidatosGobernador, self.candidatosPresidencia)

    def run(self):
        """
        Funcion para ejecutar los votos al servidor
        """
        pool = ThreadPoolExecutor(self.concurrency)
        print("Empezando Pool")
        url = ''
        body = {}
        for count, votante in enumerate(self.votantes.values()):
            address = votante['address']
            localidad = votante['location']
            candidatoPresi = random.choice(self.candidatosPresidencia)
            candidatoGob = random.choice(self.candidatosGobernador.get(localidad, [None]))
            url = f"http://{self.centros[0][0]}:{self.centros[0][1]}/api/votar/"
            body = {
                'address': address,
                'localidad': localidad,
                'presidente': candidatoPresi,
                'gobernador': candidatoGob
            }
            pool.submit(self.test, count, address, localidad, candidatoPresi, candidatoGob, url)
        
        print("Listo")

    def test(self, count, address, localidad, candidatoPresi, candidatoGob, url):
        # time.sleep(0.1)
        # body del votante
        body = {
            'address': address,
            'localidad': localidad,
            'presidente': candidatoPresi,
            'gobernador': candidatoGob
        }

        # Enviar la peticion
        response = requests.post(url, data=json.dumps(body))
        print("Hilo ", count, response)


if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some file.')
    parser.add_argument('-n', type=str, help='Archivo de Centros de Votacion')
    parser.add_argument('-nc', type=str, help="Numero de concurrencia")
    args = parser.parse_args()

    generator = GeneradorVotos(args.n, args.nc)
    generator.run()