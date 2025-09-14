Security Best Practices Applied

This document lists security settings and changes made in the project:

1. settings.py
- DEBUG should be False in production.
- SECURE_BROWSER_XSS_FILTER = True enables the browser XSS filter.
- X_FRAME_OPTIONS = 'DENY' prevents clickjacking.
- SECURE_CONTENT_TYPE_NOSNIFF = True prevents MIME-type sniffing.
- CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE ensure cookies are sent only over HTTPS.
- HSTS settings added for production (SECURE_HSTS_SECONDS, ...).
- Simple CSP middleware added in `LibraryProject/middleware.py` to set a conservative Content-Security-Policy header.

2. Templates
- All forms should include {% csrf_token %}. Example added in `bookshelf/templates/bookshelf/form_example.html`.

3. Views and Forms
- Added `bookshelf/forms.py` with `BookForm` to validate and clean input data.
- Views updated to use `BookForm` and `get_object_or_404` for safe retrieval.

4. Notes & Next Steps
- Install `django-csp` for an established CSP solution and add it to INSTALLED_APPS to manage policies more fully.
- Set DEBUG=False and configure HTTPS before enabling HSTS in production.
- Consider adding more form validation and server-side sanitization for user-generated content.
