import os
import json
from .config import ABI, HTTP_SERVER, CONTRACT_ADDRESS
from web3 import Web3, HTTPProvider
from flask import Flask, request, render_template
from flask.wrappers import Response
from flask_cors import CORS

PATH = os.path.dirname(os.path.realpath(__name__))

# Config
app = Flask(__name__)
CORS(app)

# Conexion con el contrato
w3 = Web3(HTTPProvider(HTTP_SERVER))
contract = w3.eth.contract( address = CONTRACT_ADDRESS, abi = ABI)

############ HTML ##############

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


############# API ##############

@app.route("/api/obtener-votar/", methods=['POST'])
def ir_votar() -> Response:
    data =request.get_json(force=True) 
    address = data.get('address')
    print(address)
    # Obtener el votando con el address
    # (id, nombre, localidad, centroVotacion)
    votante = contract.functions.getVotante(address).call()
    
    print(votante)
    # Buscar candidatos segun la localidad
    # [(id, nombre, localidad, cargo, votos), ...]
    candidatosPresi = contract.functions.getCandidatos(votante[2], 0).call()
    candidatosGob = contract.functions.getCandidatos(votante[2], 1).call()

    # Armar el dict
    elecciones = {
        'presidente': [],
        'gobernador': [],
        'localidad': votante[2]
    }

    for candidato in candidatosPresi:
        elecciones['presidente'].append([candidato[0], candidato[1]])

    for candidato in candidatosGob:
        elecciones['gobernador'].append([candidato[0], candidato[1]])

    return Response(json.dumps(elecciones))


@app.route("/api/votar/", methods=['POST'])
def registrar_voto() -> Response:
    data = request.get_json(force=True) 
    address = data.get('address')
    localidad = data.get('localidad')
    candidatoPresi = data.get('presidente')
    candidatoGob = data.get('gobernador')
    
    if candidatoPresi == 'null':
        candidatoPresi = Web3.toHex(0)
    if candidatoGob == 'null':
        candidatoGob = Web3.toHex(0)

    print(address, localidad, candidatoPresi, candidatoGob)
    
    try:
        contract.functions.votar(localidad, candidatoPresi, candidatoGob).transact({'from': address})
    except Exception as e:
        print(e)
        return Response(json.dumps({"error": "Error" }), status=400)

    return Response(json.dumps({"message":"Se ha registrado el voto"}), status=200)


@app.route("/api/resultados/", methods=['GET'])
def resultados() -> Response:
    resultados = contract.functions.reporteGanadores().call()
    
    return Response(json.dumps(resultados), status=200)