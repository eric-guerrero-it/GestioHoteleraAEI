-- Procediment per netejar dades de targetes després de 7 dies del checkout
CREATE OR REPLACE PROCEDURE netejar_targetes()
LANGUAGE plpgsql AS $$
BEGIN
  UPDATE pagament
  SET num_targeta = 'XXXX-XXXX-XXXX-0000'
  WHERE dni_client IN (
    SELECT dni_client
    FROM reserva
    WHERE dataFinal < CURRENT_DATE - INTERVAL '7 days'
  );
END;
$$;

-- Trigger que executa la neteja després d’un checkout
CREATE OR REPLACE FUNCTION trigger_neteja_targetes()
RETURNS TRIGGER AS $$
BEGIN
  CALL netejar_targetes();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_neteges_targetes
AFTER UPDATE ON reserva
FOR EACH ROW
WHEN (NEW.dataFinal IS NOT NULL)
EXECUTE FUNCTION trigger_neteja_targetes();
