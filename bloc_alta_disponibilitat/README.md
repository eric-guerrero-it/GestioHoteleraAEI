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

## 👥 Autors

**Grup 12 – AEI**  
ASIX – INS Sa Palomera  
Curs 2024/2025

---

## 🔗 Repositori principal

➡️ [Torna al projecte principal](../README.md)
