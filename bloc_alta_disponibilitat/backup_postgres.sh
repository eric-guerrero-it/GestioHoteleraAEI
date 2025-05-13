#!/bin/bash

# Script: backup_postgres.sh
# Descripció: fa una còpia física completa del node principal
# Autor: Grup 12 - AEI Espamus+
# Data: 2025-05-13

DATA=$(date +%Y%m%d_%H%M)
DEST="/backups_postgres/backup_$DATA"
PGUSER="replicador"
PGPASS="replica123"
export PGPASSWORD=$PGPASS

mkdir -p "$DEST"

pg_basebackup -h 10.94.254.76 -U $PGUSER -D "$DEST" -Ft -z -P --wal-method=stream

if [ $? -eq 0 ]; then
  echo "[OK] Backup realitzat correctament a $DEST"
else
  echo "[ERROR] Error en fer el backup"
fi
