import argparse
import json
import random
from random import randint
from wallet import Wallet
from subprocess import call

class Votantes():
    # Directorio de identidades
    
    def __init__(self):
        self.num_voters = 0

    def choose_candidates(dict, voters_key, puesto, porcentaje=1):
        candidatos_email = random.sample(voters_key, (len(voters_key)*porcentaje)//100)
        for j in range(len(candidatos_email)):
                dict[candidatos_email[j]].update({'candidato':puesto})

    @classmethod
    def generate_votantes(cls, file):
        Lines = file.readlines()

        voters = cls()
        num_voters = 0
        count = 0

        # Dict for storing voters
        wallets = {}
        wallet_json = {}

        localidades = set()

        for line in Lines:
            linea_temp = line.strip().split()

            voters_key = []

            location = linea_temp[0]
            localidades.add(location)
            voters_by_location = int(linea_temp[1])
            voting_centers = int(linea_temp[2])

            num_voters += voters_by_location

            for i in range(voters_by_location):
                # Generar identidades random
                person = Wallet.generate_random_person()
                # Crear claves
                person.generate_keys()
                # Introducir en el arreglo de candidatos_gobernador
                voters_key.append(person.email)
                # Save person
                wallets[person.email] = person
                wallet_json[person.email] = {
                    "full_name": person.get_full_name(),
                    "name": person.name,
                    "last name": person.lastname,
                    "location": location,
                    "votingCenter": random.randint(1, voting_centers),
                    "privateKey": person.privkey,
                    "publicKey": person.pubkey,
                    "address": person.address,
                    "checksum_address": person.checksum_address,
                    "balance": 10000000,

                    # 0==No candidato, 1==candidato presidencia, 2==candidato gobernador
                    "candidato": 0,
                }
                print(f"Generating wallet {count}")
                count += 1
            
            # Select candidatos a gobernador de location
            cls.choose_candidates(wallet_json, voters_key, 2)

        # Seleccionar candidatos a presidencia
        cls.choose_candidates(wallet_json, list(wallet_json.keys()), 1)


        # Escribir los votantes
        with open('wallets.json', 'w+') as file:
            text = json.dumps(wallet_json, indent = 3)
            file.write(text)
        
        # Escribir las localidades
        with open('localidades.txt', 'w+') as file:
            l = ''
            for i in localidades:
                l += f"{i}\n"
            file.write(l[:-1])
        

        # Guardar Wallets
        voters.wallets = wallets

        # Guardar voters
        voters.num_voters = num_voters


        print(f"GENERATED {len(voters.wallets)} WALLETS")

if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some file.')
    parser.add_argument('-f', type=argparse.FileType('r+'), help='Archivo de localidades')
    args = parser.parse_args()

    generator = Votantes.generate_votantes(args.f)