
-- SCRIPT SQL: Creació de taules per a la gestió hotelera ESPAMUS+. Grup12 AEI

-- Taula principal dels hotels registrats
CREATE TABLE IF NOT EXISTS HOTEL (
    idHotel SERIAL PRIMARY KEY,  -- Identificador únic generat automàticament
    nom VARCHAR(100) NOT NULL,
    estrelles SMALLINT CHECK (estrelles BETWEEN 1 AND 5),  -- Validació d’estrelles
    adreca VARCHAR(150),
    poblacio VARCHAR(100),
    web VARCHAR(100),
    telefon VARCHAR(20)
);

-- Persones registrades al sistema (clients i treballadors)
CREATE TABLE IF NOT EXISTS PERSONA (
    dni VARCHAR(15) PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    cognoms VARCHAR(100) NOT NULL,
    telefon VARCHAR(20),
    adreca VARCHAR(150),
    dataNaixement DATE CHECK (dataNaixement < CURRENT_DATE)
);

-- Clients derivats de PERSONA
CREATE TABLE IF NOT EXISTS CLIENT (
    dni VARCHAR(15) PRIMARY KEY REFERENCES PERSONA(dni)
);

-- Treballadors derivats de PERSONA
CREATE TABLE IF NOT EXISTS TREBALLADOR (
    dni VARCHAR(15) PRIMARY KEY REFERENCES PERSONA(dni),
    tipusTreballador VARCHAR(50) NOT NULL  -- Ex: "cuina", "recepció", etc.
);

-- Personal de recepció amb atributs propis
CREATE TABLE IF NOT EXISTS RECEPCIO (
    dni VARCHAR(15) PRIMARY KEY REFERENCES TREBALLADOR(dni),
    anysExperiencia SMALLINT CHECK (anysExperiencia >= 0)
);

-- Personal de cuina amb atributs especialitzats
CREATE TABLE IF NOT EXISTS CUINA (
    dni VARCHAR(15) PRIMARY KEY REFERENCES TREBALLADOR(dni),
    categoria VARCHAR(50) CHECK (categoria IN ('xef', 'cuiner 1a', 'cuiner 2a', 'ajudant de cuina')),
    darrerLlocTreball VARCHAR(100),
    revisatPer VARCHAR(15),
    CONSTRAINT fk_cuina_revisat FOREIGN KEY (revisatPer) REFERENCES CUINA(dni)
);

-- Resta del personal (restaurant, activitats, neteja...)
CREATE TABLE IF NOT EXISTS RESTAPersonal (
    dni VARCHAR(15) PRIMARY KEY REFERENCES TREBALLADOR(dni)
);

-- Llistat d’idiomes gestionats al sistema
CREATE TABLE IF NOT EXISTS IDIOMA (
    nom VARCHAR(50) PRIMARY KEY
);

-- Coneixement d’idiomes per treballador amb nivell
CREATE TABLE IF NOT EXISTS CONEIXEMENT (
    dni VARCHAR(15) REFERENCES TREBALLADOR(dni),
    nomIdioma VARCHAR(50) REFERENCES IDIOMA(nom),
    parla VARCHAR(20) CHECK (parla IN ('malament','regular','bé','molt bé','perfecte')),
    enten VARCHAR(20) CHECK (enten IN ('malament','regular','bé','molt bé','perfecte')),
    escriu VARCHAR(20) CHECK (escriu IN ('malament','regular','bé','molt bé','perfecte')),
    PRIMARY KEY (dni, nomIdioma)  -- PK composta: un treballador no pot repetir idioma
);

-- Serveis disponibles als hotels (massatges, bugaderia, etc.)
CREATE TABLE IF NOT EXISTS SERVEI (
    idServei SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    cost NUMERIC(8,2) NOT NULL CHECK (cost >= 0)
);

-- Relació N:M entre hotels i serveis oferts
CREATE TABLE IF NOT EXISTS HOTEL_SERVEI (
    idHotel INT REFERENCES HOTEL(idHotel) ON DELETE CASCADE,
    idServei INT REFERENCES SERVEI(idServei),
    PRIMARY KEY (idHotel, idServei)
);

-- Cada hotel té múltiples habitacions amb dades tècniques
CREATE TABLE IF NOT EXISTS HABITACIO (
    idHabitacio SERIAL PRIMARY KEY,
    numero SMALLINT NOT NULL,  -- Número visible de l’habitació (101, 202, etc.)
    llits SMALLINT CHECK (llits >= 1),
    m2 NUMERIC(5,2) CHECK (m2 > 0),
    teNevera BOOLEAN DEFAULT FALSE,
    teTelevisio BOOLEAN DEFAULT FALSE,
    idHotel INT REFERENCES HOTEL(idHotel)  -- FK cap a l’hotel propietari
);

-- Activitats disponibles als hotels per a clients
CREATE TABLE IF NOT EXISTS ACTIVITAT (
    idActivitat SERIAL PRIMARY KEY,
    idHotel INT REFERENCES HOTEL(idHotel) ON DELETE CASCADE,  -- Activitat associada a un hotel
    nom VARCHAR(100) NOT NULL,
    descripcio TEXT,
    data DATE,
    preu NUMERIC(6,2) CHECK (preu >= 0)
);

-- Relació de treballadors assignats a un hotel
CREATE TABLE IF NOT EXISTS TREBALLA (
    idHotel INT REFERENCES HOTEL(idHotel),
    dniTreballador VARCHAR(15) REFERENCES TREBALLADOR(dni),
    PRIMARY KEY (idHotel, dniTreballador)
);

-- Reserves fetes per clients amb dates i hotel
CREATE TABLE IF NOT EXISTS RESERVA (
    idReserva SERIAL PRIMARY KEY,
    dataInici DATE NOT NULL,
    dataFinal DATE NOT NULL CHECK (dataFinal > dataInici),
    idHotel INT REFERENCES HOTEL(idHotel),
    dniClient VARCHAR(15) REFERENCES CLIENT(dni)
);

-- Assignació d’habitacions a una reserva amb preus
CREATE TABLE IF NOT EXISTS RESERVA_HABITACIO (
    idReserva INT REFERENCES RESERVA(idReserva),
    idHabitacio INT REFERENCES HABITACIO(idHabitacio),
    preuTemporadaAlta NUMERIC(8,2) NOT NULL CHECK (preuTemporadaAlta > 0),
    preuTemporadaBaixa NUMERIC(8,2) NOT NULL CHECK (preuTemporadaBaixa > 0),
    PRIMARY KEY (idReserva, idHabitacio)
);

-- Sol·licituds de serveis per part de clients
CREATE TABLE IF NOT EXISTS SOLLICITUD (
    idSollicitud SERIAL PRIMARY KEY,
    dataHora TIMESTAMP NOT NULL,
    idHotel INT REFERENCES HOTEL(idHotel),
    idServei INT REFERENCES SERVEI(idServei),
    dniClient VARCHAR(15) REFERENCES CLIENT(dni),
    pagarEnCheckOut BOOLEAN DEFAULT TRUE
);

-- Factures generades a check-out
CREATE TABLE IF NOT EXISTS FACTURA (
    idFactura SERIAL PRIMARY KEY,
    dataEmissio DATE NOT NULL,
    importTotal NUMERIC(10,2) NOT NULL CHECK (importTotal >= 0),
    dniClient VARCHAR(15) REFERENCES CLIENT(dni)
);

-- Relació entre factures i serveis consumits
CREATE TABLE IF NOT EXISTS FACTURA_SERVEI (
    idFactura INT REFERENCES FACTURA(idFactura),
    idSollicitud INT REFERENCES SOLLICITUD(idSollicitud),
    PRIMARY KEY (idFactura, idSollicitud)
);

CREATE TABLE enviaments_api (
    id SERIAL PRIMARY KEY,
    data_hora TIMESTAMP DEFAULT now(),
    estat TEXT,
    json_enviat JSONB
);

