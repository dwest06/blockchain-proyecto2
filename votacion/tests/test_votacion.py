from brownie import accounts, Votacion
from brownie.network import account
import pytest

@pytest.fixture
def contract():
    return Votacion.deploy("TestVotacion", {'from': accounts[0].address})

@pytest.fixture
def contract_localidades(contract, owner):
    contract.registrarLocalidad("Caracas", 10, {'from': owner.address})
    # contract.registrarLocalidad("Zulia", 5, {'from': owner.address})

@pytest.fixture
def contract_votantes(contract, contract_localidades, owner):
    contract.registrarVotante(owner.address, "Votante1", "Caracas", {'from': owner.address})
    contract.registrarVotante(accounts[1].address, "Votante2", "Caracas", {'from': owner.address})

@pytest.fixture
def contract_full(contract, contract_votantes, owner):
    contract.registrarCandidato(owner.address, "Candidato1", 0, "Caracas", {'from': owner.address})
    contract.registrarCandidato(accounts[1].address, "Candidato1", 1, "Caracas", {'from': owner.address})
    # contract.registrarCandidato(accounts[2].address, "Candidato1", 1, "Zulia", {'from': owner.address})

@pytest.fixture
def owner():
    return accounts[0]

def test_deploy_insta(contract):
    assert contract.balance() == 0

def test_owner_contract(contract, owner):
    assert contract.owner() == owner.address

def test_reinicializar_votacion(contract):
    nuevo_nombre ="OtraVotacion"
    contract.reinicializar(nuevo_nombre)
    assert contract.nombreVotacion() == nuevo_nombre

def test_votacion_abierta(contract):
    assert contract.votacionAbierta() == True

def test_cerrar_votacion(contract, owner):
    contract.cerrarVotacion({'from': owner.address})
    assert contract.votacionAbierta() == False

def test_registrar_localidad(contract, owner):
    nombre = "Caracas"
    contract.registrarLocalidad(nombre, 10, {'from': owner.address})
    assert contract.localidades(0)[0] == nombre 

def test_getLocalidades(contract, owner):
    contract.registrarLocalidad("Caracas", 10, {'from': owner.address})
    contract.registrarLocalidad("Zulia", 5, {'from': owner.address})
    assert len(contract.getLocalidades()) == 2

def test_registrar_votantes(contract, contract_localidades, owner):
    contract.registrarVotante(owner.address, "Votante1", "Caracas", {'from': owner.address})
    contract.registrarVotante(accounts[1].address, "Votante2", "Caracas", {'from': owner.address})

    assert contract.votantes(0)[0] == owner.address
    assert contract.votantes(1)[0] == accounts[1].address

def test_registrar_candidatos_presidente(contract, contract_votantes, owner):
    contract.registrarCandidato(owner.address, "Candidato1", 0, "Caracas", {'from': owner.address})

    candPresi = contract.getCandidatos("Caracas", 0)
    assert len(candPresi) == 1
    assert candPresi[0][0] == owner.address

# @pytest.mark.skip(reason="No esta funcionando registrar candidato gobernador")
def test_registrar_candidatos_gobernador(contract, contract_votantes, owner):
    contract.registrarCandidato(accounts[1].address, "Candidato1", 1, "Caracas", {'from': owner.address})

    candGob = contract.getCandidatos("Caracas", 1, {'from': owner.address})
    assert len(candGob) == 1
    assert candGob[0][0] == accounts[1].address

def test_votar(contract, contract_full, owner):
    votante = contract.getVotante(owner.address, {'from': owner.address})
    localidad = votante[2]
    candPresi = contract.getCandidatos(localidad, 0, {'from': owner.address})
    candGob = contract.getCandidatos(localidad, 1, {'from': owner.address})
    contract.votar(localidad, candPresi[0][0], candGob[0][0], {'from': owner.address})
    # contract.votar(localidad, candPresi[0][0], accounts[1].address, {'from': owner.address})

def test_reporte_ganadores(contract, contract_full, owner):
    # Mismo proceso de votar
    votante = contract.getVotante(owner.address, {'from': owner.address})
    localidad = votante[2]
    candPresi = contract.getCandidatos(localidad, 0, {'from': owner.address})
    candGob = contract.getCandidatos(localidad, 1, {'from': owner.address})
    contract.votar(localidad, candPresi[0][0], candGob[0][0], {'from': owner.address})
    # contract.votar(localidad, candPresi[0][0], accounts[1].address, {'from': owner.address})

    # Cerrar votacion
    contract.cerrarVotacion({'from': owner.address})

    # Obtener reporte 
    ganadores = contract.reporteGanadores()

    print(ganadores)
    ganadorPresi = ganadores[0]
    ganadoresGob = ganadores[1]

    # El owner es el candidato a la presidencia que deberia ganar
    assert ganadorPresi[0] == owner.address
    assert ganadorPresi[4] == 1

    for cand in ganadoresGob:
        if cand[2] == "Caracas":
            assert cand[0] == accounts[1].address
            assert cand[4] == 1
        elif cand[2] == "Zulia":
            assert cand[0] == accounts[2].address
            assert cand[4] == 1
        else:
            assert False
    
