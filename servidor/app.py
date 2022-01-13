import os
import json
from .abi import abi as ABI
from web3 import Web3, HTTPProvider
from flask import Flask, request, render_template
from flask.wrappers import Response
from flask_cors import CORS

PATH = os.path.dirname(os.path.realpath(__name__))

# Config
app = Flask(__name__)
CORS(app)

rpc_server = os.environ.get('HTTP_SERVER', 'http://127.0.0.1:8545/')
CONTRACT_ADDRESS = os.environ.get("CONTRACT_ADDRESS", None)

w3 = Web3(HTTPProvider(rpc_server))

contract = w3.eth.contract( address = CONTRACT_ADDRESS, abi = ABI)

# Utils
def send_to_blockchain(transaction):
    pass

def generate_transaction(address, votacion, candidato):
    pass

############ HTML ##############

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


############# API ##############

@app.route("/api/localidades/", methods=['GET'])
def localidades() -> Response:
    # Conectarse al SC y obtener las localidades registradas
    localidades = ['Caracas', 'Carabobo', 'Zulia', 'Aragua']
    return Response(json.dumps(localidades))

@app.route("/api/votar/<string:localidad>/", methods=['POST'])
def ir_votar(localidad: str) -> Response:
    address = request.form.get('address')

    elecciones = {
        'presidente': [
            'Candidato1',
            'Candidato2',
            'Candidato3'
        ],
        "gobernador": [
            'Candidato1',
            'Candidato2',
            'Candidato3'
        ]
    }
    # Buscar candidatos segun la localidad


    return Response(json.dumps(elecciones))


@app.route("/api/votar/", methods=['POST'])
def registrar_voto() -> Response:
    data = request.get_json(force=True) 
    address = data.get('address')
    localidad = data.get('localidad')
    candidatoPresi = data.get('presidente')
    candidatoGob = data.get('gobernador')
    print(address, localidad, candidatoPresi, candidatoGob)

    # Generar la transaccion dado los datos del votante
    # transaction = generate_transaction(address, votacion, candidato)

    # Enviar la transaccion a la blockchain
    # send_to_blockchain(transaction)

    return Response(json.dumps("Se ha registrado el voto"), status=200)
