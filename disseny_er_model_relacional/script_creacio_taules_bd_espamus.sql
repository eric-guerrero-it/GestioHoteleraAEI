
-- SCRIPT SQL: Creació de taules per a la gestió hotelera ESPAMUS+. Grup12 AEI

-- Taula principal dels hotels
CREATE TABLE IF NOT EXISTS HOTEL (
    idHotel SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    estrelles SMALLINT CHECK (estrelles BETWEEN 1 AND 5),
    adreca VARCHAR(200),
    poblacio VARCHAR(150),
    web VARCHAR(150),
    telefon VARCHAR(30)
);

-- Persones registrades al sistema (clients i treballadors)
CREATE TABLE IF NOT EXISTS PERSONA (
    dni VARCHAR(20) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    cognoms VARCHAR(150) NOT NULL,
    telefon VARCHAR(30),
    adreca VARCHAR(200),
    nacionalitat VARCHAR(100),
    dataNaixement DATE CHECK (dataNaixement < CURRENT_DATE)
);

-- Clients vinculats a PERSONA
CREATE TABLE IF NOT EXISTS CLIENT (
    dni VARCHAR(20) PRIMARY KEY REFERENCES PERSONA(dni) ON DELETE CASCADE,
    chat_id TEXT
);

-- Treballadors vinculats a PERSONA
CREATE TABLE IF NOT EXISTS TREBALLADOR (
    dni VARCHAR(20) PRIMARY KEY REFERENCES PERSONA(dni) ON DELETE CASCADE,
    tipusTreballador VARCHAR(100) NOT NULL
);

-- Personal de recepció
CREATE TABLE IF NOT EXISTS RECEPCIO (
    dni VARCHAR(20) PRIMARY KEY REFERENCES TREBALLADOR(dni) ON DELETE CASCADE,
    anysExperiencia SMALLINT CHECK (anysExperiencia >= 0)
);

-- Personal de cuina
CREATE TABLE IF NOT EXISTS CUINA (
    dni VARCHAR(20) PRIMARY KEY REFERENCES TREBALLADOR(dni) ON DELETE CASCADE,
    categoria VARCHAR(50) CHECK (categoria IN ('xef', 'cuiner 1a', 'cuiner 2a', 'ajudant de cuina')),
    darrerLlocTreball VARCHAR(200),
    revisatPer VARCHAR(20),
    CONSTRAINT fk_cuina_revisat FOREIGN KEY (revisatPer) REFERENCES CUINA(dni) ON DELETE SET NULL
);

-- Resta del personal (restaurant, activitats, neteja...)
CREATE TABLE IF NOT EXISTS RESTAPersonal (
    dni VARCHAR(20) PRIMARY KEY REFERENCES TREBALLADOR(dni) ON DELETE CASCADE
);

-- Idiomes disponibles
CREATE TABLE IF NOT EXISTS IDIOMA (
    nom VARCHAR(100) PRIMARY KEY
);

-- Coneixement d’idiomes per treballador
CREATE TABLE IF NOT EXISTS CONEIXEMENT (
    dni VARCHAR(20) REFERENCES TREBALLADOR(dni) ON DELETE CASCADE,
    nomIdioma VARCHAR(100) REFERENCES IDIOMA(nom) ON DELETE CASCADE,
    parla VARCHAR(20) CHECK (parla IN ('malament','regular','bé','molt bé','perfecte')),
    enten VARCHAR(20) CHECK (enten IN ('malament','regular','bé','molt bé','perfecte')),
    escriu VARCHAR(20) CHECK (escriu IN ('malament','regular','bé','molt bé','perfecte')),
    PRIMARY KEY (dni, nomIdioma)
);

-- Serveis disponibles als hotels
CREATE TABLE IF NOT EXISTS SERVEI (
    idServei SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    cost NUMERIC(8,2) NOT NULL CHECK (cost >= 0)
);

-- Relació N:M entre hotels i serveis
CREATE TABLE IF NOT EXISTS HOTEL_SERVEI (
    idHotel INT REFERENCES HOTEL(idHotel) ON DELETE CASCADE,
    idServei INT REFERENCES SERVEI(idServei) ON DELETE CASCADE,
    PRIMARY KEY (idHotel, idServei)
);

-- Habitacions d'un hotel
CREATE TABLE IF NOT EXISTS HABITACIO (
    idHabitacio SERIAL PRIMARY KEY,
    numero SMALLINT NOT NULL,
    llits SMALLINT CHECK (llits >= 1),
    m2 NUMERIC(5,2) CHECK (m2 > 0),
    teNevera BOOLEAN DEFAULT FALSE,
    teTelevisio BOOLEAN DEFAULT FALSE,
    idHotel INT REFERENCES HOTEL(idHotel) ON DELETE CASCADE
);

-- Activitats dels hotels
CREATE TABLE IF NOT EXISTS ACTIVITAT (
    idActivitat SERIAL PRIMARY KEY,
    idHotel INT REFERENCES HOTEL(idHotel) ON DELETE CASCADE,
    nom VARCHAR(150) NOT NULL,
    descripcio TEXT,
    data DATE,
    preu NUMERIC(6,2) CHECK (preu >= 0)
);

-- Assignació de treballadors a hotels
CREATE TABLE IF NOT EXISTS TREBALLA (
    idHotel INT REFERENCES HOTEL(idHotel) ON DELETE CASCADE,
    dniTreballador VARCHAR(20) REFERENCES TREBALLADOR(dni) ON DELETE CASCADE,
    PRIMARY KEY (idHotel, dniTreballador)
);

-- Reserves realitzades per clients
CREATE TABLE IF NOT EXISTS RESERVA (
    idReserva SERIAL PRIMARY KEY,
    dataInici DATE NOT NULL,
    dataFinal DATE NOT NULL CHECK (dataFinal > dataInici),
    idHotel INT REFERENCES HOTEL(idHotel) ON DELETE CASCADE,
    dniClient VARCHAR(20) REFERENCES CLIENT(dni) ON DELETE CASCADE
);

-- Habitacions assignades a reserves
CREATE TABLE IF NOT EXISTS RESERVA_HABITACIO (
    idReserva INT REFERENCES RESERVA(idReserva) ON DELETE CASCADE,
    idHabitacio INT REFERENCES HABITACIO(idHabitacio) ON DELETE CASCADE,
    preuTemporadaAlta NUMERIC(8,2) NOT NULL CHECK (preuTemporadaAlta > 0),
    preuTemporadaBaixa NUMERIC(8,2) NOT NULL CHECK (preuTemporadaBaixa > 0),
    PRIMARY KEY (idReserva, idHabitacio)
);

-- Sol·licituds de serveis dels clients
CREATE TABLE IF NOT EXISTS SOLLICITUD (
    idSollicitud SERIAL PRIMARY KEY,
    dataHora TIMESTAMP NOT NULL,
    idHotel INT REFERENCES HOTEL(idHotel) ON DELETE CASCADE,
    idServei INT REFERENCES SERVEI(idServei) ON DELETE CASCADE,
    dniClient VARCHAR(20) REFERENCES CLIENT(dni) ON DELETE CASCADE,
    pagarEnCheckOut BOOLEAN DEFAULT TRUE
);

-- Factures generades
CREATE TABLE IF NOT EXISTS FACTURA (
    idFactura SERIAL PRIMARY KEY,
    dataEmissio DATE NOT NULL,
    importTotal NUMERIC(10,2) NOT NULL CHECK (importTotal >= 0),
    dniClient VARCHAR(20) REFERENCES CLIENT(dni) ON DELETE CASCADE
);

-- Relació entre factures i serveis consumits
CREATE TABLE IF NOT EXISTS FACTURA_SERVEI (
    idFactura INT REFERENCES FACTURA(idFactura) ON DELETE CASCADE,
    idSollicitud INT REFERENCES SOLLICITUD(idSollicitud) ON DELETE CASCADE,
    PRIMARY KEY (idFactura, idSollicitud)
);

-- Registre dels enviaments a l'API externa
CREATE TABLE IF NOT EXISTS ENVIAMENTS_API (
    id SERIAL PRIMARY KEY,
    data_hora TIMESTAMP DEFAULT now(),
    estat TEXT,
    json_enviat JSONB
);
