from brownie import accounts
import json

VOTANTES_FILE = './wallets.json'
WEI = 10000000
a0 = accounts[0]

# Leer Json de Votantes
file = open(VOTANTES_FILE, 'r')
votantes = json.loads(file.read())

# Transferir desde la cuenta 0 a las demas cuentas
for i in votantes.values():
    x = accounts.add(i['privateKey'])
    a0.transfer(x.address, WEI)


for i in votantes.values():
    print(accounts.at(i['address']))

