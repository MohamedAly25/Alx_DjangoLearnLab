Security Overview — advanced_features_and_security

This project has implemented a set of security best practices for Django. Summary:

1) settings.py
- DEBUG: Should be False in production. Keep True only in development.
- SECURE_BROWSER_XSS_FILTER = True
- X_FRAME_OPTIONS = 'DENY'
- SECURE_CONTENT_TYPE_NOSNIFF = True
- CSRF_COOKIE_SECURE = True (set when serving over HTTPS)
- SESSION_COOKIE_SECURE = True (set when serving over HTTPS)
- HSTS: SECURE_HSTS_SECONDS, SECURE_HSTS_INCLUDE_SUBDOMAINS, SECURE_HSTS_PRELOAD
- Simple CSP middleware added at `LibraryProject/middleware.py` to set a conservative Content-Security-Policy header.

2) Templates
- All form templates include `{% csrf_token %}`. See `bookshelf/templates/bookshelf/form_example.html`.
- Output in templates is escaped using the `|escape` filter where appropriate.

3) Views & Forms
- Views use Django ORM methods (`filter`, `get_object_or_404`) instead of raw SQL.
- Input validation is handled with Django forms (`bookshelf/forms.py`) — see `BookForm` and `ExampleForm`.
- Permissions enforced using `@permission_required` decorators on views.

4) How to test
- Try submitting a form without a CSRF token — Django should return 403.
- Test a search with a payload like "' OR 1=1" — ORM filters will treat this as a literal string, not SQL.
- Test XSS by entering `<script>alert(1)</script>` in inputs: Django auto-escapes outputs and CSP middleware helps block inline scripts.

5) Next steps
- Install and configure `django-csp` for a more robust CSP policy management.
- Configure HTTPS for production and then enable HSTS and secure cookies.
- Add automated tests for CSRF, form validation, and permission checks.

6) HTTPS enforcement (added)
- `SECURE_SSL_REDIRECT = True` has been set in `settings.py` to redirect HTTP -> HTTPS.
- `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, and `SECURE_HSTS_PRELOAD` are configured.
- `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and `SESSION_COOKIE_SAMESITE`/`CSRF_COOKIE_SAMESITE` are set to help protect cookies.
- `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` is set so Django recognizes proxied HTTPS requests.

See `DEPLOYMENT_HTTPS.md` for detailed instructions on obtaining TLS certificates (Let's Encrypt + Certbot) and example Nginx/Apache configurations. Be sure to set `DEBUG = False` and add your domain to `ALLOWED_HOSTS` before enabling these in production.
