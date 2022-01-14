from brownie import accounts
import json
import os

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__name__))))

VOTANTES_FILE = '/wallets.json'
WEI = 10000000
a0 = accounts[0]

def main():
    # Leer Json de Votantes
    file = open(path + VOTANTES_FILE, 'r')
    votantes = json.loads(file.read())

    # Transferir desde la cuenta 0 a las demas cuentas
    for i in votantes.values():
        x = accounts.add(i['privateKey'])
        a0.transfer(x.address, WEI)

    # Imprimir resultados
    for i in votantes.values():
        print(accounts.at(i['checksum_address']), accounts.at(i['checksum_address']).balance())
