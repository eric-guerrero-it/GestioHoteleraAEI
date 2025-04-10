
-- SCRIPT SQL: Creació de la base de dades per a la gestió hotelera ESPAMUS+. Grup12 AEI

CREATE DATABASE gestiohoteleraei
WITH 
    ENCODING 'UTF8'  -- Permet l’emmagatzematge de caràcters de molts idiomes
    LC_COLLATE = 'en_US.UTF-8'  -- Ordre alfabètic per operacions de comparació de text
    LC_CTYPE = 'en_US.UTF-8'    -- Comportament dels caràcters (majúscules, tipus ...)
    TEMPLATE template0;
