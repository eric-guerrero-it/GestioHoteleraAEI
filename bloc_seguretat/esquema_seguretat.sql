-- ─────────────────────────────────────────────
-- ESQUEMA DE SEGURETAT: Rols i permisos per Espamus+
-- Desenvolupat pel Grup 12 – AEI
-- ─────────────────────────────────────────────

-- 1. Crear rols
CREATE ROLE admin_hotel LOGIN PASSWORD 'admin123';
CREATE ROLE gestor_recepcio LOGIN PASSWORD 'recepcio123';
CREATE ROLE treballador_recepcio LOGIN PASSWORD 'trabrec123';
CREATE ROLE gestor_serveis LOGIN PASSWORD 'serveis123';
CREATE ROLE gestor_habitacions LOGIN PASSWORD 'habitacions123';
CREATE ROLE analista_dades LOGIN PASSWORD 'analista123';
CREATE ROLE usuari_temporal LOGIN PASSWORD 'temporal123';

-- 2. Assignar permisos a cada rol

-- Admin: pot fer de tot
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_hotel;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_hotel;

-- Gestor recepció
GRANT SELECT, INSERT, UPDATE ON CLIENT, RESERVA, RESERVA_HABITACIO, FACTURA TO gestor_recepcio;

-- Treballador recepció
GRANT SELECT, INSERT ON CLIENT, RESERVA, FACTURA TO treballador_recepcio;

-- Gestor serveis
GRANT SELECT, INSERT, UPDATE ON SERVEI, SOLLICITUD, FACTURA_SERVEI TO gestor_serveis;

-- Gestor habitacions
GRANT SELECT, UPDATE ON HABITACIO TO gestor_habitacions;

-- Analista (només pot consultar)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analista_dades;

-- Usuari temporal
GRANT SELECT ON HOTEL, HABITACIO TO usuari_temporal;

-- 3. Permisos futurs: heretar automàticament si es creen noves taules
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO analista_dades;

