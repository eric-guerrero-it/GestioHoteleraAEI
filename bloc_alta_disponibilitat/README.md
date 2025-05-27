# Bloc d’Alta Disponibilitat – Gestió Hotelera Espamus+

Aquest mòdul implementa la infraestructura d'alta disponibilitat i còpies de seguretat per al sistema de gestió hotelera **Espamus+**.  
Assegura la **continuïtat del servei 24x7**, la **resiliència a fallades** i la **recuperació de dades**.

---

## Objectius

- Garantir la **disponibilitat contínua** del servei.
- Permetre **recuperació davant fallades** o errors humans.
- Assegurar **consistència entre nodes** mitjançant replicació.
- Automatitzar còpies de seguretat sense aturar el sistema.

---

## Requisit 1 – Infraestructura de Maquinari

### Nodes de base de dades (actiu-passiu)

| Component          | Node Primari (Actiu)         | Node Rèplica (Passiu)       |
|--------------------|------------------------------|-----------------------------|
| **CPU**            | 6 vCPU Xeon/EPYC             | 6 vCPU Xeon/EPYC            |
| **RAM**            | 16 GB DDR4                   | 16 GB DDR4                  |
| **Emmagatzematge** | 2x SSD NVMe 250 GB (RAID1)   | 2x SSD NVMe 250 GB (RAID1)  |
| **Sistema Operatiu** | Ubuntu Server 22.04 LTS    | Ubuntu Server 22.04 LTS     |
| **Xarxa**          | 1 Gbps Ethernet              | 1 Gbps Ethernet             |
| **Rol**            | PostgreSQL actiu + SSL       | PostgreSQL hot standby + SSL|

### Servidor de Backups

| Component        | Valor                                 |
|------------------|----------------------------------------|
| **CPU**          | 2 vCPU                                |
| **RAM**          | 4 GB DDR4                             |
| **Disc**         | 500 GB HDD (amb compressió ZFS)       |
| **Sistema**      | Ubuntu Server 22.04 LTS               |
| **Rol**          | Execució de còpies de seguretat i restauracions |

---

## Requisit 2 – Rèplica de Base de Dades

### Tipus de replicació

- PostgreSQL **Streaming Replication**
- Mode **actiu-passiu** amb fitxer `standby.signal`

### Verificació de l’estat

```sql
-- Al node primari:
SELECT * FROM pg_stat_replication;

-- Al node secundari:
SELECT pg_is_in_recovery();  -- Ha de retornar true
```

## Simulació de failover

```bash
# 1. Aturar el node principal
sudo systemctl stop postgresql

# 2. Promocionar el node rèplica
sudo -u postgres pg_ctlcluster 14 main promote
```

---

## Requisit 3 – Sistema de Còpies de Seguretat

### Còpia física (hot backup) amb `pg_basebackup`

```bash
#!/bin/bash
DATA=$(date +%Y%m%d_%H%M)
DEST="/backups_postgres/backup_$DATA"
export PGPASSWORD="replic@123"
pg_basebackup -h 10.94.254.76 -U replicador -D "$DEST" -Ft -z -P --wal-method=stream
```

###  Programació amb cron
```cron
0 3 * * * /usr/local/bin/backup_postgres.sh >> /var/log/backup_postgres.log 2>&1
```

### Validació

- Backup provat des del node secundari

- Inclou WAL per suportar recuperació puntual (PITR)

- Compatible amb entorns 24x7

---

## Requisit 4 – Eliminació Segura de Dades de Targetes

Evitem conservar dades sensibles com les targetes de crèdit després del període de retenció (**7 dies després del checkout**), seguint els principis del **RGPD**.

---

### Procediment PL/pgSQL

```sql
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
```

### Trigger associat

```sql
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
```

## 🗂️ Arxius importants

| Fitxer / Directori                   | Descripció                                        |
|--------------------------------------|---------------------------------------------------|
| `/usr/local/bin/backup_postgres.sh` | Script automatitzat de còpia de seguretat         |
| `/backups_postgres/`                | Carpeta on es desen les còpies                    |
| `postgresql.auto.conf`              | Connexió al node principal des del secundari      |
| `standby.signal`                    | Activació del mode *hot standby*                  |

### Fitxers SQL i scripts

- [`backup_postgres.sh`](./backup_postgres.sh): script automatitzat que realitza una còpia física del node principal utilitzant `pg_basebackup`, amb compressió i suport per PITR.  
  ➤ S'utilitza al Requisit 3 i està planificat via cron.

- [`neteja_targetes.sql`](./neteja_targetes.sql): fitxer que conté el procediment i trigger per netejar dades de targetes de crèdit segons RGPD.  
  ➤ Forma part del Requisit 4 (eliminació segura de dades).

---

## 👥 Autors

**Grup 12 – AEI**  
ASIX – INS Sa Palomera  
Curs 2024/2025

---

## 🔗 Repositori principal

➡️ [Torna al projecte principal](../README.md)




---

🔁 Abans de la prova (servidor secundari)

✅ PAS 1 – Crear backup

Executar al secundari:

sudo -u postgres pg_basebackup -Ft -z -D /backups_postgres/backup_$(date +%Y%m%d_%H%M) \
-X fetch -U replicador -h IP_DEL_PRINCIPAL

Verifica que s’ha creat el directori i/o arxiu .tar.gz.

Opcional: comprimir el directori si no s’ha creat com .tar.gz:

cd /backups_postgres
sudo tar -czf /tmp/backup_YYYYMMDD_HHMM.tar.gz -C backup_YYYYMMDD_HHMM .

⚠️ El professor afegeix i elimina informació

-- Afegim Francesc
INSERT INTO persona (dni, nom, cognoms, telefon, adreca, nacionalitat, dataNaixement) 
VALUES ('12345678Z', 'Francesc', 'Martínez Bonet', '999123456', 'Carrer Major 12, Girona', 'Spanish', '1985-04-12');
INSERT INTO client (dni) VALUES ('12345678Z');

-- El professor elimina:
DROP TABLE persona CASCADE;

✅ PAS 2 – Crear punt de restauració i fer checkpoint (abans del DROP si pots)

sudo -u postgres psql -d gestiohoteleraaei
CHECKPOINT;
SELECT pg_create_restore_point('abans_accio_profe');

🔄 Recuperació PITR (servidor principal)

✅ PAS 3 – Aturar PostgreSQL

sudo systemctl stop postgresql

✅ PAS 4 – Moure l’antic clúster i preparar nou

sudo mv /var/lib/postgresql/14/main /var/lib/postgresql/14/main_old
sudo mkdir -p /var/lib/postgresql/14/main
sudo chown postgres:postgres /var/lib/postgresql/14/main
sudo chmod 0700 /var/lib/postgresql/14/main

✅ PAS 5 – Copiar i descomprimir el backup

scp /tmp/backup_YYYYMMDD_HHMM.tar.gz user@IP_DEL_PRINCIPAL:/tmp/

sudo tar -xzf /tmp/backup_YYYYMMDD_HHMM.tar.gz -C /var/lib/postgresql/14/main --strip-components=1

📁 Verifica:

sudo ls /var/lib/postgresql/14/main/PG_VERSION

✅ PAS 6 – Configura restauració PITR

echo "restore_command = 'cp /var/lib/postgresql/14/wal_archive/%f %p'" | sudo tee -a /var/lib/postgresql/14/main/postgresql.auto.conf
echo "recovery_target_name = 'abans_accio_profe'" | sudo tee -a /var/lib/postgresql/14/main/postgresql.auto.conf

✅ PAS 7 – Reinicia PostgreSQL

sudo systemctl start postgresql

📜 Comprova els logs:

sudo tail -f /var/log/postgresql/postgresql-14-main.log

✅ PAS 8 – Validació

sudo -u postgres psql -d gestiohoteleraaei

-- Comprova que la taula persona i treballador existeixen:
\d persona;
\d treballador;

-- Comprova que Francesc existeix:
SELECT * FROM persona WHERE nom = 'Francesc';

✅ PAS 9 – Neteja opcional

sudo rm -rf /var/lib/postgresql/14/main_old

Aquest procediment assegura la restauració exacta al moment abans de l’acció destructiva del professor utilitzant PITR (Point In Time Recovery).
