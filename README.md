# CRM Imobiliária + WhatsApp (Meta) + IA (API) — pronto para VPS (HostGator)

Este projeto entrega:
- CRM web (Leads, Imóveis, Negócios/Funil, Tarefas)
- Gestão de usuários com papéis (**admin**, **broker**, **assistant**) e autenticação JWT
- Webhook do WhatsApp Cloud API (Meta) + envio de resposta automática
- Camada de IA (modo `rules` por padrão; você pode integrar um provedor via API)

## 1) Requisitos na VPS
- Ubuntu 22.04/24.04 (ou Debian)
- Nginx
- Python 3.10+
- PostgreSQL

## 2) Instalar dependências
```bash
sudo apt update
sudo apt install -y python3 python3-venv nginx postgresql postgresql-contrib
```

## 3) Banco de dados (PostgreSQL)
```bash
sudo -u postgres psql
CREATE DATABASE crm_db;
CREATE USER crm_user WITH PASSWORD 'crm_pass';
GRANT ALL PRIVILEGES ON DATABASE crm_db TO crm_user;
\q
```

## 4) Deploy (pasta /var/www/crm)
```bash
sudo mkdir -p /var/www/crm
sudo chown -R $USER:$USER /var/www/crm
```
Copie o conteúdo do projeto para `/var/www/crm`.

Crie venv e instale:
```bash
cd /var/www/crm/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copie `.env` para `/var/www/crm/.env` e ajuste:
- DATABASE_URL
- JWT_SECRET
- ADMIN_EMAIL/ADMIN_PASSWORD
- WHATSAPP_*

## 5) Rodar (teste)
```bash
cd /var/www/crm/backend
source venv/bin/activate
bash run.sh
```
Acesse: `http://IP-DA-VPS:8000`.

## 6) Produção com systemd + Nginx
1) Copie `scripts/systemd-crm.service` para `/etc/systemd/system/crm.service`
2) Ajuste caminhos se necessário (`/var/www/crm/backend`)

```bash
sudo systemctl daemon-reload
sudo systemctl enable crm
sudo systemctl start crm
sudo systemctl status crm
```

Nginx:
- Copie `nginx/crm.conf` para `/etc/nginx/sites-available/crm.conf`
- Ajuste `server_name SEU_DOMINIO_AQUI`
- Habilite:
```bash
sudo ln -s /etc/nginx/sites-available/crm.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Frontend:
- arquivos estão em `/var/www/crm/frontend` (HTML/CSS/JS)

## 7) Configurar Webhook WhatsApp (Meta)
- URL do webhook: `https://SEU_DOMINIO/webhook/whatsapp`
- VERIFY TOKEN: `WHATSAPP_VERIFY_TOKEN` do seu `.env`

## 8) Login
O sistema cria um admin automaticamente (seed) ao iniciar, usando variáveis do `.env`:
- ADMIN_EMAIL
- ADMIN_PASSWORD

Abra o painel: `https://SEU_DOMINIO/login.html`
