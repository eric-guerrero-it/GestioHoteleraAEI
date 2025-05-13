# 🛡️ Bloc d’Alta Disponibilitat – Gestió Hotelera Espamus+

Aquest mòdul implementa la infraestructura d'alta disponibilitat i còpies de seguretat per al sistema de gestió hotelera Espamus+. Assegura la **continuïtat del servei 24x7**, la **resistència a fallades** i la **recuperació de dades**.

---

## 🎯 Objectius

- Garantir la **disponibilitat contínua** del servei.
- Permetre **recuperació davant fallades** o errors humans.
- Assegurar **consistència entre nodes** mitjançant replicació.
- Automatitzar còpies de seguretat sense aturar el sistema.

---

## 🧰 Requisit 1 – Infraestructura de Maquinari

| Component            | Node Primari (Actiu)           | Node Rèplica (Passiu)           |
|----------------------|-------------------------------|-------------------------------|
| CPU                  | 6 vCPU Xeon/EPYC               | 6 vCPU Xeon/EPYC               |
| RAM                  | 16 GB DDR4                     | 16 GB DDR4                     |
| Emmagatzematge       | 2x SSD NVMe 250 GB (RAID1)     | 2x SSD NVMe 250 GB (RAID1)     |
| Sistema Operatiu     | Ubuntu Server 22.04 LTS        | Ubuntu Server 22.04 LTS        |
| Connexió Xarxa       | 1 Gbps Ethernet                | 1 Gbps Ethernet                |
| Rol                  | PostgreSQL actiu + SSL         | PostgreSQL hot standby + SSL   |

## 📦 **Servidor de Backups**:

| Component           | Valor                                |
|---------------------|--------------------------------------|
| **CPU**            | 2 vCPU                               |
| **RAM**            | 4 GB DDR4                            |
| **Disc**           | 500 GB HDD (amb compressió ZFS)      |
| **Sistema Operatiu** | Ubuntu Server 22.04 LTS             |
| **Rol**            | Execució de còpies de seguretat i restauracions |

---

## 🔁 Requisit 2 – Rèplica de Base de Dades

### 🔄 Tipus de replicació:
- PostgreSQL **Streaming Replication**
- Mode **actiu-passiu** amb `standby.signal`

### 📊 Verificació:
```bash
# Al node primari:
SELECT * FROM pg_stat_replication;

# Al node secundari:
SELECT pg_is_in_recovery();  -- Ha de retornar true
```

## Simulació de failover:

# 1. Aturar node principal
sudo systemctl stop postgresql

# 2. Promocionar node rèplica
sudo -u postgres pg_ctlcluster 14 main promote

### 🔁 Recuperació:
Fer `pg_basebackup` des del node actiu cap al nou rèplica.

Tornar a configurar `standby.signal`.

---

## Requisit 3 – Sistema de Còpies de Seguretat

### Còpia física (hot backup) amb pg_basebackup

```bash
#!/bin/bash
DATA=$(date +%Y%m%d_%H%M)
DEST="/backups_postgres/backup_$DATA"
export PGPASSWORD="replic@123"
pg_basebackup -h 10.94.254.76 -U replicador -D "$DEST" -Ft -z -P --wal-method=stream
```
### Programació cron:

```cron
0 3 * * * /usr/local/bin/backup_postgres.sh >> /var/log/backup_postgres.log 2>&1
```

### Validació:

- Backup verificat des del node secundari.

- Conté WAL per suportar PITR.

- Compatible amb entorns 24x7.

