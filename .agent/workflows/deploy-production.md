---
description: How to deploy FinCore CRM to production
---

# Deploying FinCore CRM to Production

This workflow guides you through deploying the FinCore CRM application to a production environment.

## Prerequisites
- A production server (Linux recommended)
- Domain name (optional but recommended)
- PostgreSQL or MySQL database (recommended for production)
- Web server (Nginx or Apache)
- WSGI server (Gunicorn recommended)

## Steps

### 1. Prepare the Production Server

**Install required packages:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
```

### 2. Set Up the Application

**Clone or upload your project to the server:**
```bash
cd /var/www/
sudo mkdir fincore-crm
sudo chown $USER:$USER fincore-crm
cd fincore-crm
```

**Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install django gunicorn psycopg2-binary
```

### 3. Configure Database

**Create PostgreSQL database:**
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE fincore_crm;
CREATE USER fincore_user WITH PASSWORD 'your_secure_password';
ALTER ROLE fincore_user SET client_encoding TO 'utf8';
ALTER ROLE fincore_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE fincore_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE fincore_crm TO fincore_user;
\q
```

### 4. Update Django Settings

**Edit `sales_crm/settings.py`:**

```python
# Set DEBUG to False
DEBUG = False

# Add your domain to ALLOWED_HOSTS
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'server-ip']

# Update database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fincore_crm',
        'USER': 'fincore_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 5. Collect Static Files and Migrate

```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

### 6. Set Up Gunicorn

**Create Gunicorn systemd service file:**
```bash
sudo nano /etc/systemd/system/fincore-crm.service
```

**Add the following content:**
```ini
[Unit]
Description=FinCore CRM Gunicorn daemon
After=network.target

[Service]
User=your-username
Group=www-data
WorkingDirectory=/var/www/fincore-crm
ExecStart=/var/www/fincore-crm/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/fincore-crm/fincore.sock \
          sales_crm.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Start and enable the service:**
```bash
sudo systemctl start fincore-crm
sudo systemctl enable fincore-crm
```

### 7. Configure Nginx

**Create Nginx configuration:**
```bash
sudo nano /etc/nginx/sites-available/fincore-crm
```

**Add the following content:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/fincore-crm;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/fincore-crm/fincore.sock;
    }
}
```

**Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/fincore-crm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Set Up SSL (Optional but Recommended)

**Install Certbot:**
```bash
sudo apt install certbot python3-certbot-nginx
```

**Obtain SSL certificate:**
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 9. Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## Post-Deployment

1. **Test the application** by visiting your domain
2. **Monitor logs:**
   - Application logs: `sudo journalctl -u fincore-crm`
   - Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. **Set up regular backups** for your database
4. **Configure monitoring** (e.g., using tools like Sentry for error tracking)

## Updating the Application

When you need to update:
```bash
cd /var/www/fincore-crm
source venv/bin/activate
git pull  # or upload new files
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart fincore-crm
```
