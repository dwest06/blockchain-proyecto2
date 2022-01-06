import os
import json
from web3 import Web3
from flask import Flask, request, render_template
from flask.wrappers import Response
from flask_cors import CORS

PATH = os.path.dirname(os.path.realpath(__name__))

# Config
app = Flask(__name__)
CORS(app)

w3 = Web3()

# Utils
def send_to_blockchain(transaction):
    pass

def generate_transaction(address, votacion, candidato):
    pass

############ HTML ##############

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/votar/", methods=['GET'])
def votacion():
    return render_template('votacion.html')


############# API ##############

@app.route("/api/localidades/", methods=['GET'])
def localidades() -> Response:
    # Conectarse al SC y obtener las localidades registradas
    localidades = ['Caracas', 'Carabobo', 'Zulia', 'Aragua']
    return Response(json.dumps(localidades))

@app.route("/api/votar/<string:localidad>/", methods=['POST'])
def ir_votar(localidad: str) -> Response:
    address = request.form.get('address')

    # Buscar candidatos segun la localidad

    return Response(json.dumps(localidades))


@app.route("/api/votar/<string:localidad>/", methods=['POST'])
def registrar_voto(localidad: str) -> Response:
    address = request.form.get('address')
    votacion = request.form.get('votacion')
    candidato = request.form.get('candidato')



    # Generar la transaccion dado los datos del votante
    transaction = generate_transaction(address, votacion, candidato)

    # Enviar la transaccion a la blockchain
    send_to_blockchain(transaction)

    return Response("Se ha registrado el voto", status=200)
