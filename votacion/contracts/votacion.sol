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
        string localidad;
        uint256 centroVotacion;
    }

    struct Candidato{
        address id;
        string nombre;
        string localidad;
        Cargo cargo;
        uint256 votos;
    }

    struct CandidatoEstadistica{
        address id;
        string nombre;
        uint256 porcentaje;
    }

    // Variables de entorno
    address public owner; // Propietario del contrato
    string public nombreVotacion; // Nombre de la Votacion
    bool public votacionAbierta; // Variable para saber si la votacion esta abierta o no
    uint256 totalVotantes; // Total de los votantes que han participado en la votacion

    // Localidades, Votantes
    mapping (string => uint) indexLocalidades;
    Localidad[] public localidades; // Lista de las localidades registradas
    mapping (address => uint) indexVotantes;
    Votante[] public votantes; // Lista de los votantes registrados
    mapping (address => bool) existeVotantes;

    // Estructuras de Votantes y Candidatos 
    mapping (string => address[]) public votantesLocalidad; // Obtener lista de Votantes de una localidad
    mapping( string => mapping (address => uint )) public indexCandidatoGobernadorLocalidad;
    mapping (string => Candidato[]) public candidatosGobernadorLocalidad; //Obtener lista de Candidatos a Gobernacion por localidad
    mapping (address => uint) public indexCandidatosPresidente;
    Candidato[] public candidatosPresidente; //Obtener lista de Candidatos a Presidencia

    // Registro de votantes 
    mapping (address => bool) public registroVotantes; // Registro de los votantes



    // Eventos
    event LocalidadRegistrada(Localidad localidad);
    event VotanteRegistrado(Votante votante);
    event CandidatoRegistrado(Candidato candidato);
    event VotacionCerrada();

    // Modifiers
    modifier isOwner(){
        require( owner == msg.sender, "Solo el propietario del contrato tiene permiso de realizar esta accion.");
        _;
    }
    modifier estaVotacionAbierta(){
        require(votacionAbierta, "Ya la votacion cerro.");
        _;
    }
    modifier isVotante(address id){
        Votante memory votante = buscarVotante(id);
        require ( votante.id > address(0) , "Esta address no se encuentra registrada como votante.");
        _;
    }
    modifier yaVoto(){
        require( !registroVotantes[msg.sender], "Ya realizo su voto.");
        _;
    }
    modifier existLocalidad(string memory nombre){
        Localidad memory localidad = buscarLocalidad(nombre);
        require(memcmp(bytes(localidad.nombre), bytes(nombre)), "Esta localidad no existe");
        _;
    }

    // UTILS
    function memcmp(bytes memory a, bytes memory b) internal pure returns(bool){
        return (a.length == b.length) && (keccak256(a) == keccak256(b));
    }

    constructor(
        string memory _nombreVotacion
    ){
        owner = msg.sender;
        reinicializar(_nombreVotacion);
    }

    /**
        @notice Inicializar o Reinicializar una votacion
        @param _nombreVotacion nombre de la Votacion
     */
    function reinicializar(
        string memory _nombreVotacion
    ) public isOwner{
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
        // TODO: Preguntar si es necesario verificar que el numero de centro sea mayor a 0
        Localidad memory localidad = Localidad(nombre, numCentros);
        localidades.push(localidad);
        uint index = localidades.length - 1;
        indexLocalidades[nombre] = index;
        emit LocalidadRegistrada(localidad);
    }

    /**
        @notice Buscar Localidad
        @param nombre nombre de la localidad a buscar
     */
    function buscarLocalidad(string memory nombre) private view returns (Localidad memory){
        uint index = indexLocalidades[nombre];
        return localidades[index];
    }

    /**
        @notice Registrar un Votante
        @param id address del Votante
        @param nombre nombre del Votante
        @param nombreLocalidad nombre de la localidad del cargo
     */
    function registrarVotante(
        address id, 
        string memory nombre, 
        string memory nombreLocalidad,
        uint256 centroVotacion
    ) public isOwner existLocalidad(nombreLocalidad){
        // Verificar que no exista el address ya registrado como votante
        require(!existeVotantes[id], "Votante ya se encuentra registrado");
        // Registrar Votante
        Votante memory votante = Votante(id, nombre, nombreLocalidad, centroVotacion);
        votantes.push(votante);
        uint index = votantes.length - 1;
        indexVotantes[id] = index;
        existeVotantes[id] = true;
        emit VotanteRegistrado(votante);
    }

    /**
        @notice Buscar Votante
        @param id address del votante a buscar
     */
    function buscarVotante(address id) private view returns (Votante memory){
        uint index = indexVotantes[id];
        return votantes[index];
    }

    /**
        @notice Registrar un Candidato
        @param id address del candidato
        @param nombre nombre del candidato
        @param cargo Cargo de la candidatura
        @param localidad localidad del cargo
     */
    function registrarCandidato(
        address id, 
        string memory nombre, 
        Cargo cargo, 
        string memory localidad
    ) public isOwner existLocalidad(localidad) isVotante(id) {
        // Verificar que que el address no exista registrado como otro votante independiente de la localidad

        // Crear el candidato
        Candidato memory candidato = Candidato(id, nombre, localidad, cargo, 0 );
        // Verificar donde guardarlo
        if( cargo == Cargo.Presidente){
            candidatosPresidente.push(candidato);
            uint index = candidatosPresidente.length - 1;
            indexCandidatosPresidente[id] = index; 
        }
        else {
            Candidato[] storage _candidatos = candidatosGobernadorLocalidad[localidad];
            _candidatos.push(candidato);
            uint index = _candidatos.length - 1;
            indexCandidatoGobernadorLocalidad[localidad][id] = index;
        }
        // Registrar el candidato
        emit CandidatoRegistrado(candidato);
    }

    /**
        @notice Buscar Candidato Presidente
        @param id address del votante a buscar
     */
    function buscarCandidatoPresidente(address id) private view returns (Candidato storage){
        uint index = indexCandidatosPresidente[id];
        return candidatosPresidente[index];
    }

    /**
        @notice Buscar Candidato Gobernador
        @param id address del votante a buscar
     */
    function buscarCandidatoGobernador(string memory localidad, address id) private view returns (Candidato storage){
        uint index = indexCandidatoGobernadorLocalidad[localidad][id];
        return candidatosGobernadorLocalidad[localidad][index];
    }

    /**
        @notice Votar
        @param localidad Nombre de la localidad
        @param idCandidatoPresidente address del candidato a votar para el puesto de Presidente
        @param idCandidatoGobernador address del candidato a votar para el puesto de gobernador de la localidad
     */
    function votar(
        string memory localidad, 
        address idCandidatoPresidente, 
        address idCandidatoGobernador
    ) public estaVotacionAbierta isVotante(msg.sender) yaVoto returns (bool){
        // Revisar voto blanco
        if (idCandidatoPresidente != address(0)){
            // Buscar Candidato a Presidente y sumarle 1 a los votos
            Candidato storage candidatoPresi = buscarCandidatoPresidente(idCandidatoPresidente);
            candidatoPresi.votos += 1;
        }

        if( idCandidatoGobernador != address(0)){
            // Buscar Candidato a Gobernador y sumarle 1 a los votos
            Candidato storage candidatoGob = buscarCandidatoGobernador(localidad, idCandidatoGobernador);
            candidatoGob.votos += 1;
        }

        // Registrar voto del votante
        registroVotantes[msg.sender] = true;
        totalVotantes += 1;
        return true;
    }

    /**
        @notice Cerrar Votacion
     */
    function cerrarVotacion() public isOwner estaVotacionAbierta{
        votacionAbierta = false;
        emit VotacionCerrada();
    }

    function obtenerGanadorPresidencia() private view returns (Candidato memory){
        // Ganador de presidencia
        Candidato memory ganadorPresidencia;
        uint mayor = 0;
        for( uint i = 0; i < candidatosPresidente.length; i+=1){
            if ( candidatosPresidente[i].votos > mayor){
                mayor = candidatosPresidente[i].votos;
                ganadorPresidencia = candidatosPresidente[i];
            }
        }
        return ganadorPresidencia;
    }

    /**
        @notice Regresar ganadores con sus porcentajes
        @return Lista Ordenada de los ganadores con su porcentaje
     */
    function reporteGanadores() public view returns (Candidato memory , Candidato[] memory ){
        // TODO: Hay que verificar que ya se haya cerrado la votacion?

        // Ganador de presidencia
        Candidato memory ganadorPresidencia = obtenerGanadorPresidencia();

        // Ganadores Gobernaciones
        uint countLocalidades = localidades.length;
        Candidato[] memory ganadoresGobernacion = new Candidato[](countLocalidades - 1);
        for( uint j = 0; j < localidades.length; j+=1){
            Localidad memory localidad = localidades[j];
            Candidato[] memory candidatos = candidatosGobernadorLocalidad[localidad.nombre];
            uint mayor = 0;
            for( uint k = 0; k < candidatos.length; k+=1){
                if (candidatos[k].votos > mayor){
                    ganadoresGobernacion[j] = (candidatos[k]);
                }
            }
        }
        return (ganadorPresidencia, ganadoresGobernacion);
    }

    /**
        @notice Generar un reporte de una localidad
        @return Lista de candidatos de una localidad
     */
    function reporteLocalidad(string memory nombreLocalidad) 
        public view existLocalidad(nombreLocalidad) returns (CandidatoEstadistica[] memory){
        Localidad memory localidad = buscarLocalidad(nombreLocalidad);

        // Lista de votantes de la localidad
        address[] memory votantesLocal = votantesLocalidad[nombreLocalidad];
        uint256 cantidadVotantesRegistrados = votantesLocal.length;

        // Estadistica Presidente


        // Estadisticas Gobernador
        uint256 cantidadVotantes = 0;
        Candidato[] memory candidatosLocal = candidatosGobernadorLocalidad[nombreLocalidad];
        CandidatoEstadistica[] memory estadisticas = new CandidatoEstadistica[](candidatosLocal.length);
        
        for( uint256 i = 0; i < candidatosLocal.length; i+=1){
            Candidato memory candidato = candidatosLocal[i];
            cantidadVotantes += candidato.votos;
            CandidatoEstadistica memory cand = CandidatoEstadistica(
                candidato.id,
                candidato.nombre,
                candidato.votos/cantidadVotantesRegistrados
            );
            estadisticas[i] = cand;
        }

        return estadisticas;

    }


    // GETTERS

    function getLocalidades() public view returns(Localidad[] memory _localidades){
        return localidades;
    }

    function getLocalidad(string memory nombre) public view returns(Localidad memory localidad){
        return buscarLocalidad(nombre);
    }

    function getCandidatos(string memory localidad, Cargo cargo) public view returns (Candidato[] memory candidats){
        if( cargo == Cargo.Presidente){
            return candidatosPresidente;
        }
        else {
            return candidatosGobernadorLocalidad[localidad];
        }   
    }

    function getVotante(address id) public view returns (Votante memory votant){
        return buscarVotante(id);
    }

}