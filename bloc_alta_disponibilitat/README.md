# 🛡️ Bloc d’Alta Disponibilitat – Gestió Hotelera Espamus+

Aquest mòdul implementa la infraestructura d'alta disponibilitat i còpies de seguretat per al sistema de gestió hotelera **Espamus+**.  
Assegura la **continuïtat del servei 24x7**, la **resiliència a fallades** i la **recuperació de dades**.

---

## 🎯 Objectius

- Garantir la **disponibilitat contínua** del servei.
- Permetre **recuperació davant fallades** o errors humans.
- Assegurar **consistència entre nodes** mitjançant replicació.
- Automatitzar còpies de seguretat sense aturar el sistema.

---

## 🧰 Requisit 1 – Infraestructura de Maquinari

### 📡 Nodes de base de dades (actiu-passiu)

| Component          | Node Primari (Actiu)         | Node Rèplica (Passiu)       |
|--------------------|------------------------------|-----------------------------|
| **CPU**            | 6 vCPU Xeon/EPYC             | 6 vCPU Xeon/EPYC            |
| **RAM**            | 16 GB DDR4                   | 16 GB DDR4                  |
| **Emmagatzematge** | 2x SSD NVMe 250 GB (RAID1)   | 2x SSD NVMe 250 GB (RAID1)  |
| **Sistema Operatiu** | Ubuntu Server 22.04 LTS    | Ubuntu Server 22.04 LTS     |
| **Xarxa**          | 1 Gbps Ethernet              | 1 Gbps Ethernet             |
| **Rol**            | PostgreSQL actiu + SSL       | PostgreSQL hot standby + SSL|

### 💾 Servidor de Backups

| Component        | Valor                                 |
|------------------|----------------------------------------|
| **CPU**          | 2 vCPU                                |
| **RAM**          | 4 GB DDR4                             |
| **Disc**         | 500 GB HDD (amb compressió ZFS)       |
| **Sistema**      | Ubuntu Server 22.04 LTS               |
| **Rol**          | Execució de còpies de seguretat i restauracions |

---

## 🔁 Requisit 2 – Rèplica de Base de Dades

### 🔄 Tipus de replicació

- PostgreSQL **Streaming Replication**
- Mode **actiu-passiu** amb fitxer `standby.signal`

### 🔍 Verificació de l’estat

```sql
-- Al node primari:
SELECT * FROM pg_stat_replication;

-- Al node secundari:
SELECT pg_is_in_recovery();  -- Ha de retornar true
```

## 🧪 Simulació de failover

```bash
# 1. Aturar el node principal
sudo systemctl stop postgresql

# 2. Promocionar el node rèplica
sudo -u postgres pg_ctlcluster 14 main promote
```

---

## 📦 Requisit 3 – Sistema de Còpies de Seguretat

### 🧰 Còpia física (hot backup) amb `pg_basebackup`

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
