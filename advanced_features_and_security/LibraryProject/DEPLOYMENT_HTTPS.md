HTTPS Deployment Guide — advanced_features_and_security

This document explains how to deploy the Django app behind HTTPS, obtain TLS certificates, and configure common web servers (Nginx and Apache) to redirect HTTP to HTTPS and proxy to the Django application.

1. Obtain certificates (Let's Encrypt with Certbot)

Example for Ubuntu/Debian with Nginx:

1. Install certbot and the nginx plugin:

   sudo apt update
   sudo apt install certbot python3-certbot-nginx

2. Run certbot (it will attempt to edit your Nginx config for you):

   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

3. Certbot will obtain certificates and configure automatic renewal.

If you're using Apache, install the apache plugin instead:

   sudo apt install certbot python3-certbot-apache
   sudo certbot --apache -d yourdomain.com -d www.yourdomain.com

Notes on firewalls:
- Ensure ports 80 and 443 are reachable from Let's Encrypt servers during issuance.

2. Nginx configuration example (reverse proxy to local gunicorn/uWSGI)

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Recommended security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "same-origin" always;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }
}

3. Apache (mod_proxy) configuration example

<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem

    # Proxy to gunicorn/uwsgi
    ProxyPreserveHost On
    ProxyRequests Off
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    RequestHeader set X-Forwarded-Proto "https"

    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "same-origin"
</VirtualHost>

4. Django settings notes

- In `LibraryProject/settings.py` we have set:
  - `SECURE_SSL_REDIRECT = True` (redirect non-HTTPS to HTTPS)
  - `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`
  - `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`
  - `SESSION_COOKIE_SAMESITE = 'Lax'` and `CSRF_COOKIE_SAMESITE = 'Lax'`
  - `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`

- Make sure `DEBUG = False` and `ALLOWED_HOSTS` include your domain before enabling these in production.
- If using a proxy (Nginx/Apache) ensure it sets `X-Forwarded-Proto: https` when proxying TLS requests so Django recognizes secure requests.

5. Renewals

- Let's Encrypt certificates renew automatically using a cron or systemd timer created by certbot. You can test renewal with:

   sudo certbot renew --dry-run

6. Troubleshooting

- After enabling `SECURE_SSL_REDIRECT`, you may get redirect loops if the proxy to Django doesn't set `X-Forwarded-Proto` correctly. Ensure `SECURE_PROXY_SSL_HEADER` matches the header your proxy sets (commonly `HTTP_X_FORWARDED_PROTO`).
- If you see cookies not sent to the browser, check `SESSION_COOKIE_SECURE`/`CSRF_COOKIE_SECURE` and ensure you're using HTTPS in the browser.

7. Additional recommendations

- Consider enabling OCSP stapling and hardening SSL ciphers.
- Use a firewall to restrict access to application server ports (keep 8000 only accessible locally).
- Consider using a managed load balancer/SSL termination if you host on cloud providers.
