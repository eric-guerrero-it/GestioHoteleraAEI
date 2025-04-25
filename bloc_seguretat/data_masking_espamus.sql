-- Exemple: Dades Personals
-- Taula real
CREATE TABLE persona (
    dni VARCHAR(15) PRIMARY KEY,
    nom VARCHAR(50),
    cognoms VARCHAR(100),
    telefon VARCHAR(20)
);

-- Vista enmascarada (només per usuaris sense permisos especials)
CREATE VIEW persona_masked AS
SELECT 
    CONCAT('XXX-', RIGHT(dni, 4)) AS dni,
    nom,
    cognoms,
    telefon
FROM persona;

-- Permisos
REVOKE ALL ON persona FROM public;
GRANT SELECT ON persona_masked TO analista_dades;

-- Exemple: Número de Targeta
-- Taula real
CREATE TABLE pagament (
    id_pagament SERIAL PRIMARY KEY,
    dni_client VARCHAR(15),
    num_targeta VARCHAR(20),
    import NUMERIC
);

-- Vista enmascarada
CREATE VIEW pagament_masked AS
SELECT 
    id_pagament,
    dni_client,
    CONCAT('**** **** **** ', RIGHT(num_targeta, 4)) AS num_targeta,
    import
FROM pagament;

-- Permisos
REVOKE ALL ON pagament FROM public;
GRANT SELECT ON pagament_masked TO analista_dades;

-- BONUS: Funció de masking personalitzat amb RLS
-- Funció per enmascarar el DNI segons el rol de l'usuari
CREATE OR REPLACE FUNCTION mask_dni(dni TEXT, user_role TEXT)
RETURNS TEXT AS $$
BEGIN
    IF user_role = 'analista_dades' THEN
        RETURN CONCAT('XXX-', RIGHT(dni, 4));
    ELSE
        RETURN dni;
    END IF;
END;
$$ LANGUAGE plpgsql;
