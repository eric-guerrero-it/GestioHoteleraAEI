-- Inserts per a la taula HOTEL
INSERT INTO HOTEL (idHotel, nom, estrelles, adreca, poblacio, web, telefon)
VALUES 
(1, 'Hotel Espamus', 5, 'Carrer de la Pau, 12', 'Barcelona', 'www.espamus.com', '933123456'),
(2, 'Hotel Meridiana', 4, 'Carrer del Sol, 23', 'Madrid', 'www.meridiana.com', '912654321');

-- Inserts per a la taula PERSONA
INSERT INTO PERSONA (dni, nom, cognoms, telefon, adreca, dataNaixement)
VALUES
('12345678A', 'Joan', 'Garcia', '611223344', 'Carrer de la Pau, 12, Barcelona', '1990-01-01'),
('23456789B', 'Maria', 'Pérez', '622334455', 'Carrer del Sol, 23, Madrid', '1985-05-12');

-- Inserts per a la taula CLIENT
INSERT INTO CLIENT (dni)
VALUES ('12345678A'), ('23456789B')
ON CONFLICT (dni) DO NOTHING;

-- Inserts per a la taula TREBALLADOR
INSERT INTO TREBALLADOR (dni, tipusTreballador)
VALUES
('12345678A', 'Recepció'),
('23456789B', 'Cuina');

-- Inserts per a la taula HABITACIO
INSERT INTO HABITACIO (idHabitacio, numero, llits, m2, teNevera, teTelevisio, idHotel)
VALUES
(1, 101, 2, 20.5, TRUE, TRUE, 1),
(2, 102, 2, 18.0, FALSE, TRUE, 1);

-- Inserts per a la taula RESERVA
INSERT INTO RESERVA (idReserva, dataInici, dataFinal, idHotel, dniClient)
VALUES
(1, '2025-04-01', '2025-04-05', 1, '12345678A'),
(2, '2025-04-10', '2025-04-12', 2, '23456789B');

-- Inserts per a la taula RESERVA_HABITACIO
INSERT INTO RESERVA_HABITACIO (idReserva, idHabitacio, preuTemporadaAlta, preuTemporadaBaixa)
VALUES
(1, 1, 150.00, 100.00),
(2, 2, 120.00, 80.00);

-- Desactivar les restriccions de les claus forànies temporalment
SET session_replication_role = replica;

-- Inserir dades a SOL·LICITUD
INSERT INTO SOLLICITUD (idSollicitud, dataHora, idHotel, idServei, dniClient, pagarEnCheckOut)
VALUES
(1, '2025-04-01 12:00:00', 1, 1, '12345678A', TRUE),
(2, '2025-04-10 14:00:00', 2, 2, '23456789B', FALSE);

-- Reactivar les restriccions de les claus forànies
SET session_replication_role = origin;

-- Inserts per a la taula FACTURA
INSERT INTO FACTURA (idFactura, dataEmissio, importTotal, dniClient)
VALUES
(1, '2025-04-05', 500.00, '12345678A'),
(2, '2025-04-12', 350.00, '23456789B');

-- Inserts per a la taula FACTURA_SERVEI
INSERT INTO FACTURA_SERVEI (idFactura, idSollicitud)
VALUES
(1, 1),
(2, 2);

-- Assignar els treballadors als hotels
INSERT INTO TREBALLA (dnitreballador, idHotel)
VALUES 
('12345678A', 1),  
('23456789B', 2);

-- Nova reserva per l'hotel amb idHotel = 1
INSERT INTO RESERVA (idReserva, dataInici, dataFinal, idHotel, dniclient)
VALUES (3, '2025-05-15', '2025-05-17', 1, '12345678A');
