from brownie import accounts, Votacion
from web3 import Web3, HTTPProvider
import json
import os

# ENV VARS
HTTP_SERVER = 'http://127.0.0.1:8545/'
ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
VOTANTES_FILE = '/wallets.json'
WEI = 10000000
OWNER = accounts[0]

# FONDEAR CUENTAS
def fondear_cuentas():
    # Leer Json de Votantes
    file = open(ABSOLUTE_PATH + VOTANTES_FILE, 'r')
    votantes = json.loads(file.read())

    # Transferir desde la cuenta 0 a las demas cuentas
    for i in votantes.values():
        x = accounts.add(i['privateKey'])
        OWNER.transfer(x.address, WEI)

    # Imprimir resultados
    for i in votantes.values():
        print(accounts.at(i['checksum_address']), accounts.at(i['checksum_address']).balance())


# LOCALIDADES
def store_localidades(contract):
    localidades = []
    with open(ABSOLUTE_PATH + '/localidades.txt', 'r') as file:
        for i in file.read().split('\n'):
            localidades.append(i)

    # Ingresar Localidades
    try: 
        for localidad in localidades:
            contract.functions.registrarLocalidad(localidad, 10).transact({'from': OWNER.address})
    except Exception as e:
        print("Error cargando Localidades: ", e)

    print("Localidades Cargadas")

# VOTANTES
def store_votantes(contract):
    # Leer Json de Votantes
    file = open(ABSOLUTE_PATH + VOTANTES_FILE, 'r')
    votantes = json.loads(file.read())
    try:
        for i in votantes.values():
            contract.functions.registrarVotante(
                i['checksum_address'],
                i['full_name'],
                i['location'],
                1
            ).transact({'from': OWNER.address})
    except Exception as e:
        print("Error cargando Votantes: ", e)

    print("Votantes Cargados")

# CANDIDATOS
def store_candidatos(contract):

    # Leer Json de Votantes
    file = open(ABSOLUTE_PATH + VOTANTES_FILE, 'r')
    votantes = json.loads(file.read())

    candidatosPresidencia = []
    candidatosGobernador = {}

    for votante in votantes.values():
        if int(votante.get('candidato')) == 1:
            candidatosPresidencia.append(votante)
        elif int(votante.get('candidato')) == 2:
            localidad = votante.get('localidad')
            aux = candidatosGobernador.get(localidad)
            if not aux:
                candidatosGobernador[localidad] = [] 
            candidatosGobernador[localidad].append(votante)

    try:
        # Presidente
        for i in candidatosPresidencia:
            contract.functions.registrarCandidato(
                i['checksum_address'],
                i['full_name'],
                0,
                i['location'],
            ).transact({'from': OWNER.address})
    except Exception as e:
        print("Error cargando candidatos a Presidencia: ", e)

    print("Candidatos a Presidencia Cargados")

    try:
        # Gobernador
        for i in candidatosGobernador.values():
            for j in i:
                contract.functions.registrarCandidato(
                    j['checksum_address'],
                    j['full_name'],
                    1,
                    j['location'],
                ).transact({'from': OWNER.address})
    except Exception as e:
        print("Error cargando candidatos a Gobernacion: ", e)

    print("Candidatos a Gobernacion Cargados")



def main():
    print("Creando votacion: Deploy del Contrato con el Owner")
    v = Votacion.deploy("Votacion", {'from': accounts[0].address})

    print("Fondear Cuentas Iniciales")
    fondear_cuentas()

    print("Conectando con el contrato")
    # Conexion con el contrato
    w3 = Web3(HTTPProvider(HTTP_SERVER))
    contract = w3.eth.contract( address = v.address, abi = v.abi)
    
    print("Enviando registros a Contracto (Escena Electoral)")
    store_localidades(contract)
    store_votantes(contract)
    store_candidatos(contract)

    print("Inicializacion del entorno Listo")