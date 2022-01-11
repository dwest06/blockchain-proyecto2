import argparse
import json
from wallet import Wallet
from subprocess import call

class Votantes():
    # Directorio de identidades
    
    def __init__(self):
        self.num_identities = 0

    @classmethod
    def generate_votantes(cls, file):
        Lines = file.readlines()

        identities = cls()
        num_identities = 0
        count = 0

        # Dict for storing identities
        wallets = {}
        wallet_json = {}

        for line in Lines:
            lineaTemp = line.strip().split()
            #print("Line{}: {}".format(count, lineaTemp))

            numVotantes = int(lineaTemp[1])
            num_identities += numVotantes

            for i in range(numVotantes):
                # Generar identidades random
                person = Wallet.generate_random_person()
                # Crear claves
                person.generate_keys()
                # Save person
                wallets[person.email] = person
                wallet_json[person.email] = {
                    "name": person.name,
                    "address": person.address,
                    "Localidad": lineaTemp[0]
                }
                print(f"Generating wallet {count}")
                count += 1


        with open('wallets.json', 'w+') as file:
            text = json.dumps(wallet_json)
            file.write(text)

        # Guardar Wallets
        identities.wallets = wallets

        # Guardar Identities
        identities.num_identities = num_identities


        print(f"GENERATED {len(identities.wallets)} WALLETS")

if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some file.')
    parser.add_argument('file', type=argparse.FileType('r+'), help='Archivo de localidades')
    args = parser.parse_args()

    generator = Votantes.generate_votantes(args.file)