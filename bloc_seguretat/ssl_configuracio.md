## 3️⃣ Connexió SSL – Justificació i Configuració

Per tal de garantir la seguretat de les dades emmagatzemades a la base de dades del projecte **Gestió Hotelera Espamus+**, hem configurat l'accés a **PostgreSQL** mitjançant connexions segures amb **SSL** (Secure Sockets Layer). Aquesta mesura ajuda a evitar la intercepció de dades delicades durant la comunicació entre el client i el servidor, especialment quan es tracta d'informació personal o financera com les dades dels clients i les targetes de crèdit.

📚 [Documentació oficial de PostgreSQL - SSL](https://www.postgresql.org/docs/current/ssl-tcp.html)

---

### 1.1 Generació dels certificats

S’han generat un certificat i una clau privada autofirmats amb **OpenSSL**:

```bash
# Generar la clau privada
openssl genrsa -out server.key 2048

# Establir permisos segurs
chmod 600 server.key
chown postgres:postgres server.key

# Generar el certificat autofirmat
openssl req -new -x509 -days 365 -key server.key -out server.crt
````

A continuació, els fitxers server.key i server.crt s'han mogut a la carpeta:

```bash
/etc/ssl/private/
````

---

### 1.2 Configuració de PostgreSQL

Edició del fitxer postgresql.conf per activar SSL:

```bash
ssl = on
ssl_cert_file = '/etc/ssl/private/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'
````

Edició del fitxer pg_hba.conf per obligar connexions segures:

```bash
hostssl all all 10.94.254.76 scram-sha-256
````

Un cop realitzada la configuració, s’ha reiniciat el servei:

```bash
sudo systemctl restart postgresql
````

---

### 2️⃣ Renovació Automàtica de Certificats

Per garantir la continuïtat del servei segur, hem creat un sistema de renovació periòdica dels certificats SSL.

#### Script `renew_ssl_cert.sh`

El següent script genera nous certificats, els reemplaça i reinicia PostgreSQL automàticament:

```bash
#!/bin/bash

# Generar nova clau privada
openssl genrsa -out /etc/ssl/private/server.key 2048

# Generar certificat autofirmat vàlid per 365 dies
openssl req -new -x509 -days 365 -key /etc/ssl/private/server.key -out /etc/ssl/certs/server.crt -subj "/CN=localhost"

# Establir permisos segurs
chmod 600 /etc/ssl/private/server.key
chown postgres:postgres /etc/ssl/private/server.key

# Reiniciar PostgreSQL per aplicar el nou certificat
systemctl restart postgresql
````

Aquest script es guarda a:

```bash
/usr/local/bin/renew_ssl_cert.sh
````

--- 

### Programació automàtica amb cron

Per executar automàticament la renovació cada 300 dies, afegim aquesta entrada al crontab:

```bash
0 3 */300 * * /usr/local/bin/renew_ssl_cert.sh
````

Aquesta acció:

 🔁 Es fa cada 300 dies  
  
 ⏰ A les 3:00h del matí  
  
 🔐 Es fa sense intervenció manual  
  
 🔄 Reinicia automàticament PostgreSQL amb els nous certificats  

---
