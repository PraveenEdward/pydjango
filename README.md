# Inventory Management System

A web-based Inventory Management System built with **Python and Django**.

## Features

- Product Management
- Category Management
- Customer Management
- Supplier Management
- Stock In / Stock Out
- Sales and Invoices
- Inventory Tracking
- Reports
- Excel Import / Export
- PDF Invoice
- Dashboard
- Django Admin

## Technologies

- Python
- Django
- HTML, CSS, JavaScript
- Bootstrap / AdminLTE
- MySQL
- Git / GitHub
- Gunicorn
- Nginx

---

# Installation

## 1. Clone the Project

```bash
git clone <repo-url>
cd <project-folder>
```

Example:

```bash
git clone https://github.com/username/project.git
cd project
```

## 2. Install Python Packages

Ubuntu:

```bash
sudo apt update -y
sudo apt install -y python3-venv python3-dev
sudo apt install -y pkg-config default-libmysqlclient-dev build-essential
```

## 3. Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

## 4. Install Requirements

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# Environment Variables

## 5. Create `.env`

```bash
nano .env
```

Add:

```env
DJANGO_SECRET_KEY=your-secret-key

DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_database_host
DB_PORT=3306
```

For local MySQL:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
```

For Amazon RDS:

```env
DB_HOST=your-rds-endpoint
DB_PORT=3306
```

**Do not upload `.env` to GitHub.**

Add to `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
db.sqlite3
```

---

# Database Setup

## 6. Check Django

```bash
python manage.py check
```

## 7. Create Migrations

```bash
python manage.py makemigrations
```

## 8. Apply Migrations

```bash
python manage.py migrate
```

## 9. Create Admin User

```bash
python manage.py createsuperuser
```

---

# Static Files

## 10. Create Static Directory

```bash
sudo mkdir -p /var/www/pydjango
```

Set permissions:

```bash
sudo chown -R ubuntu:www-data /var/www/pydjango
sudo chmod -R 775 /var/www/pydjango
```

## 11. Collect Static Files

```bash
python manage.py collectstatic
```

Static files will be stored in:

```text
/var/www/pydjango/
```

---

# Development

## 12. Run Django

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

For server access:

```bash
python manage.py runserver 0.0.0.0:8000
```

> Use `runserver` for development only. Use Gunicorn and Nginx for production.

---

# Production Deployment

Production flow:

```text
Browser
   |
   v
Nginx :80
   |
   v
Gunicorn :8000
   |
   v
Django
   |
   v
MySQL / RDS
```

---

# Gunicorn

## 13. Create Gunicorn Service

```bash
sudo nano /etc/systemd/system/pydjango.service
```

Add:

```ini
[Unit]
Description=Django Gunicorn Application
After=network.target

[Service]
User=ubuntu
Group=www-data

WorkingDirectory=/home/ubuntu/pydjangoserver
EnvironmentFile=/home/ubuntu/pydjangoserver/.env

ExecStart=/home/ubuntu/pydjangoserver/.venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    config.wsgi:application

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## 14. Start Gunicorn

```bash
sudo systemctl daemon-reload
sudo systemctl enable pydjango
sudo systemctl start pydjango
```

Check:

```bash
sudo systemctl status pydjango
```

Test:

```bash
curl http://127.0.0.1:8000
```

---

# Nginx

## 15. Install Nginx

```bash
sudo apt update
sudo apt install -y nginx
```

## 16. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/pydjango
```

Add:

```nginx
server {
    listen 80;
    server_name _;

    location /static/ {
        alias /var/www/pydjango/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 17. Enable Nginx Site

```bash
sudo ln -s /etc/nginx/sites-available/pydjango /etc/nginx/sites-enabled/pydjango
```

## 18. Test Nginx

```bash
sudo nginx -t
```

## 19. Enable and Reload Nginx

```bash
sudo systemctl enable nginx
sudo systemctl reload nginx
```

Check:

```bash
sudo systemctl status nginx
```

---

# Test Application

Test Gunicorn:

```bash
curl http://127.0.0.1:8000
```

Test Nginx:

```bash
curl http://127.0.0.1
```

Open in browser:

```text
http://<server-public-ip>/
```

Admin:

```text
http://<server-public-ip>/admin/
```

---

# AWS EC2

For AWS EC2, allow HTTP in the Security Group:

```text
Protocol: TCP
Port: 80
Source: 0.0.0.0/0
```

For HTTPS:

```text
Protocol: TCP
Port: 443
Source: 0.0.0.0/0
```

Do **not** expose Gunicorn port `8000` publicly.

Gunicorn should listen on:

```text
127.0.0.1:8000
```

---

# Useful Commands

## Django

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

## Gunicorn

```bash
sudo systemctl status pydjango
sudo systemctl restart pydjango
sudo journalctl -u pydjango -f
```

## Nginx

```bash
sudo nginx -t
sudo systemctl status nginx
sudo systemctl reload nginx
```

## Check Ports

```bash
sudo ss -lntp | grep -E ':80|:8000'
```

Expected:

```text
Nginx     -> :80
Gunicorn  -> 127.0.0.1:8000
```

---

# Project Structure

```text
pydjangoserver/
│
├── .venv/
├── .env
├── manage.py
├── requirements.txt
├── config/
├── backend/
├── products/
├── settings/
├── static/
└── README.md
```

Production static files:

```text
/var/www/pydjango/
```

---

# Database

Development:

```text
SQLite
```

Production:

```text
MySQL / Amazon RDS
```

---

# Security

- Keep `.env` private
- Never commit `.env` to GitHub
- Use strong database passwords
- Do not expose port `8000`
- Use HTTPS in production
- Keep the Django secret key private

---

# Author

**Jackson S**

Django Inventory Management System
