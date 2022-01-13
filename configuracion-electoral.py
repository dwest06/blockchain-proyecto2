import json
from web3 import Web3, HTTPProvider
# from .config import ABI, HTTP_SERVER, CONTRACT_ADDRESS
VOTANTES_FILE = './wallets.json'
HTTP_SERVER = 'http://127.0.0.1:8545/'
CONTRACT_ADDRESS = '0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87'
ABI = [
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "_nombreVotacion",
                'type': "string"
            }
        ],
        'name': "constructor",
        'stateMutability': "nonpayable",
        'type': "constructor"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'components': [
                    {
                        'internalType': "address",
                        'name': "id",
                        'type': "address"
                    },
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "string",
                        'name': "localidad",
                        'type': "string"
                    },
                    {
                        'internalType': "enum Votacion.Cargo",
                        'name': "cargo",
                        'type': "uint8"
                    },
                    {
                        'internalType': "uint256",
                        'name': "votos",
                        'type': "uint256"
                    }
                ],
                'indexed': False,
                'internalType': "struct Votacion.Candidato",
                'name': "candidato",
                'type': "tuple"
            }
        ],
        'name': "CandidatoRegistrado",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'components': [
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "uint256",
                        'name': "numCentros",
                        'type': "uint256"
                    }
                ],
                'indexed': False,
                'internalType': "struct Votacion.Localidad",
                'name': "localidad",
                'type': "tuple"
            }
        ],
        'name': "LocalidadRegistrada",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [],
        'name': "VotacionCerrada",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'components': [
                    {
                        'internalType': "address",
                        'name': "id",
                        'type': "address"
                    },
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "string",
                        'name': "localidad",
                        'type': "string"
                    },
                    {
                        'internalType': "uint256",
                        'name': "centroVotacion",
                        'type': "uint256"
                    }
                ],
                'indexed': False,
                'internalType': "struct Votacion.Votante",
                'name': "votante",
                'type': "tuple"
            }
        ],
        'name': "VotanteRegistrado",
        'type': "event"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "",
                'type': "string"
            },
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'name': "candidatosGobernadorLocalidad",
        'outputs': [
            {
                'internalType': "address",
                'name': "id",
                'type': "address"
            },
            {
                'internalType': "string",
                'name': "nombre",
                'type': "string"
            },
            {
                'internalType': "string",
                'name': "localidad",
                'type': "string"
            },
            {
                'internalType': "enum Votacion.Cargo",
                'name': "cargo",
                'type': "uint8"
            },
            {
                'internalType': "uint256",
                'name': "votos",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'name': "candidatosPresidente",
        'outputs': [
            {
                'internalType': "address",
                'name': "id",
                'type': "address"
            },
            {
                'internalType': "string",
                'name': "nombre",
                'type': "string"
            },
            {
                'internalType': "string",
                'name': "localidad",
                'type': "string"
            },
            {
                'internalType': "enum Votacion.Cargo",
                'name': "cargo",
                'type': "uint8"
            },
            {
                'internalType': "uint256",
                'name': "votos",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "cerrarVotacion",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "localidad",
                'type': "string"
            },
            {
                'internalType': "enum Votacion.Cargo",
                'name': "cargo",
                'type': "uint8"
            }
        ],
        'name': "getCandidatos",
        'outputs': [
            {
                'components': [
                    {
                        'internalType': "address",
                        'name': "id",
                        'type': "address"
                    },
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "string",
                        'name': "localidad",
                        'type': "string"
                    },
                    {
                        'internalType': "enum Votacion.Cargo",
                        'name': "cargo",
                        'type': "uint8"
                    },
                    {
                        'internalType': "uint256",
                        'name': "votos",
                        'type': "uint256"
                    }
                ],
                'internalType': "struct Votacion.Candidato[]",
                'name': "candidats",
                'type': "tuple[]"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "nombre",
                'type': "string"
            }
        ],
        'name': "getLocalidad",
        'outputs': [
            {
                'components': [
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "uint256",
                        'name': "numCentros",
                        'type': "uint256"
                    }
                ],
                'internalType': "struct Votacion.Localidad",
                'name': "localidad",
                'type': "tuple"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "getLocalidades",
        'outputs': [
            {
                'components': [
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "uint256",
                        'name': "numCentros",
                        'type': "uint256"
                    }
                ],
                'internalType': "struct Votacion.Localidad[]",
                'name': "_localidades",
                'type': "tuple[]"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "id",
                'type': "address"
            }
        ],
        'name': "getVotante",
        'outputs': [
            {
                'components': [
                    {
                        'internalType': "address",
                        'name': "id",
                        'type': "address"
                    },
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "string",
                        'name': "localidad",
                        'type': "string"
                    },
                    {
                        'internalType': "uint256",
                        'name': "centroVotacion",
                        'type': "uint256"
                    }
                ],
                'internalType': "struct Votacion.Votante",
                'name': "votant",
                'type': "tuple"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "",
                'type': "string"
            },
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'name': "indexCandidatoGobernadorLocalidad",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'name': "indexCandidatosPresidente",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'name': "localidades",
        'outputs': [
            {
                'internalType': "string",
                'name': "nombre",
                'type': "string"
            },
            {
                'internalType': "uint256",
                'name': "numCentros",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "nombreVotacion",
        'outputs': [
            {
                'internalType': "string",
                'name': "",
                'type': "string"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "owner",
        'outputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "id",
                'type': "address"
            },
            {
                'internalType': "string",
                'name': "nombre",
                'type': "string"
            },
            {
                'internalType': "enum Votacion.Cargo",
                'name': "cargo",
                'type': "uint8"
            },
            {
                'internalType': "string",
                'name': "localidad",
                'type': "string"
            }
        ],
        'name': "registrarCandidato",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "nombre",
                'type': "string"
            },
            {
                'internalType': "uint256",
                'name': "numCentros",
                'type': "uint256"
            }
        ],
        'name': "registrarLocalidad",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "id",
                'type': "address"
            },
            {
                'internalType': "string",
                'name': "nombre",
                'type': "string"
            },
            {
                'internalType': "string",
                'name': "nombreLocalidad",
                'type': "string"
            },
            {
                'internalType': "uint256",
                'name': "centroVotacion",
                'type': "uint256"
            }
        ],
        'name': "registrarVotante",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'name': "registroVotantes",
        'outputs': [
            {
                'internalType': "bool",
                'name': "",
                'type': "bool"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "_nombreVotacion",
                'type': "string"
            }
        ],
        'name': "reinicializar",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "reporteGanadores",
        'outputs': [
            {
                'components': [
                    {
                        'internalType': "address",
                        'name': "id",
                        'type': "address"
                    },
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "string",
                        'name': "localidad",
                        'type': "string"
                    },
                    {
                        'internalType': "enum Votacion.Cargo",
                        'name': "cargo",
                        'type': "uint8"
                    },
                    {
                        'internalType': "uint256",
                        'name': "votos",
                        'type': "uint256"
                    }
                ],
                'internalType': "struct Votacion.Candidato",
                'name': "",
                'type': "tuple"
            },
            {
                'components': [
                    {
                        'internalType': "address",
                        'name': "id",
                        'type': "address"
                    },
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "string",
                        'name': "localidad",
                        'type': "string"
                    },
                    {
                        'internalType': "enum Votacion.Cargo",
                        'name': "cargo",
                        'type': "uint8"
                    },
                    {
                        'internalType': "uint256",
                        'name': "votos",
                        'type': "uint256"
                    }
                ],
                'internalType': "struct Votacion.Candidato[]",
                'name': "",
                'type': "tuple[]"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "nombreLocalidad",
                'type': "string"
            }
        ],
        'name': "reporteLocalidad",
        'outputs': [
            {
                'components': [
                    {
                        'internalType': "address",
                        'name': "id",
                        'type': "address"
                    },
                    {
                        'internalType': "string",
                        'name': "nombre",
                        'type': "string"
                    },
                    {
                        'internalType': "uint256",
                        'name': "porcentaje",
                        'type': "uint256"
                    }
                ],
                'internalType': "struct Votacion.CandidatoEstadistica[]",
                'name': "",
                'type': "tuple[]"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "votacionAbierta",
        'outputs': [
            {
                'internalType': "bool",
                'name': "",
                'type': "bool"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'name': "votantes",
        'outputs': [
            {
                'internalType': "address",
                'name': "id",
                'type': "address"
            },
            {
                'internalType': "string",
                'name': "nombre",
                'type': "string"
            },
            {
                'internalType': "string",
                'name': "localidad",
                'type': "string"
            },
            {
                'internalType': "uint256",
                'name': "centroVotacion",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "",
                'type': "string"
            },
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'name': "votantesLocalidad",
        'outputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "string",
                'name': "localidad",
                'type': "string"
            },
            {
                'internalType': "address",
                'name': "idCandidatoPresidente",
                'type': "address"
            },
            {
                'internalType': "address",
                'name': "idCandidatoGobernador",
                'type': "address"
            }
        ],
        'name': "votar",
        'outputs': [
            {
                'internalType': "bool",
                'name': "",
                'type': "bool"
            }
        ],
        'stateMutability': "nonpayable",
        'type': "function"
    }
]

# Conexion con el contrato
w3 = Web3(HTTPProvider(HTTP_SERVER))
contract = w3.eth.contract( address = CONTRACT_ADDRESS, abi = ABI)

localidades = []
# Localidades
with open('localidades.txt', 'r') as file:
    for i in file.read().split('\n'):
        localidades.append(i)


# Leer Json de Votantes
file = open(VOTANTES_FILE, 'r')
votantes = json.loads(file.read())

# Candidatos
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

print(localidades, candidatosPresidencia)