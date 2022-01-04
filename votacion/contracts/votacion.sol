// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract Votacion {

    // Enums
    enum Cargo { Presidente, Gobernador }

    // Estructuras
    struct Localidad {
        string nombre;
        uint256 numCentros;
    }

    struct Votante{
        address id;
        string nombre;
        Localidad localidad;
        bool yaVoto;
    }

    struct Candidato{
        address id;
        string nombre;
        uint256 votos;
        Cargo cargo;
        Localidad localidad;
    }

    // Variables de entorno
    string public nombreVotacion; // Nombre de la Votacion
    bool public votacionAbierta; // Variable para saber si la votacion esta abierta o no
    uint256 totalVotantes; // Total de los votantes
    Localidad[] public localidades; // Lista de las localidades registradas
    Candidato[] public candidatos; // Lista de los candidatos registrados
    Votante[] public votantes; // Lista de los votantes registrados

    // OJOPELAO
    mapping (address => Votante) public registroVotantes; // Registro de los votantes

    address public owner; // Propietario del contrato

    // Eventos
    event LocalidadRegistrada(Localidad localidad);
    event VotanteRegistrado(Votante votante);
    event CandidatoRegistrado(Candidato candidato);
    event VotacionCerrada();
    // event VotoRegistrado();

    // Modifiers
    modifier isOwner(){
        require( owner == msg.sender, "Solo el propietario del contrato tiene permiso de realizar esta accion");
        _;
    }

    // OJOPELAO
    modifier yaVoto(Votante memory votante){
        require(!votante.yaVoto, "Ya votaste");
        _;
    }

    modifier estaVotacionAbierta(){
        require(votacionAbierta, "Ya la votacion cerro");
        _;
    }
    constructor(
        string memory _nombreVotacion
    ){
        owner = msg.sender;
        reinizializar(_nombreVotacion);
    }

    /**
        @notice Inicializar o Reinicializar una votacion
        @param _nombreVotacion nombre de la Votacion
     */
    function reinizializar(
        string memory _nombreVotacion
    ) public isOwner{
        // NOTE: Verificar si hay que borrar las Localidades, Votantes y Candidatos previamente guardados
        // Probablemente los Candidatos y Votantes si, pero las Localidades hay que preguntar

        totalVotantes = 0;
        nombreVotacion = _nombreVotacion;
        votacionAbierta = true;
    }

    /**
        @notice Registrar una nueva localidad
        @param nombre nombre de la nueva localidad
        @param numCentros numero de centros de votacion disponibles en la nueva localidad
     */
    function registrarLocalidad(string memory nombre, uint numCentros) public isOwner{
        Localidad memory localidad = Localidad(nombre, numCentros);
        localidades.push(localidad);
        emit LocalidadRegistrada(localidad);
    }

    /**
        @notice Registrar un Candidato
        @param id address del candidato
        @param nombre nombre del candidato
        @param cargo Cargo de la candidatura
        @param nombreLocalidad nombre de la localidad del cargo
     */
    function registrarCandidato(address id, string memory nombre, Cargo cargo, string memory nombreLocalidad) public isOwner{
    }

    /**
        @notice Buscar Localidad
        @param nombre nombre de la localidad a buscar
     */
    function buscarLocalidad(string memory nombre) private returns ( Localidad memory){
    }

    /**
        @notice Registrar un Votante
        @param id address del Votante
        @param nombre nombre del Votante
        @param nombreLocalidad nombre de la localidad del cargo
     */
    function registrarVotante(address id, string memory nombre, string memory nombreLocalidad) public isOwner{

    }

    /**
        @notice Votar
        @param candidato address del candidato a votar
     */
    function votar(address candidato) public estaVotacionAbierta returns (bool){
    }

    /**
        @notice Cerrar Votacion
     */
    function cerrarVotacion() public isOwner estaVotacionAbierta{
        votacionAbierta = false;
        emit VotacionCerrada();
    }

    /**
        @notice Regresar ganadores con sus porcentajes
        @return Lista Ordenada de los ganadores con su porcentaje
     */
    function reporteGanadores() public returns (bool){
    }

    /**
        @notice Generar un reporte de los ganadores de una localidad
        @return Lista de candidatos de una localidad
     */
    function reporteLocalidad(string memory localidad) public returns (bool){
    }
}