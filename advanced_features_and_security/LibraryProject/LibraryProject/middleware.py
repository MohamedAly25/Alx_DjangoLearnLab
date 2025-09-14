from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class SimpleCSPMiddleware(MiddlewareMixin):
    """Basic CSP middleware that applies a content-security-policy header."""

    def process_response(self, request, response):
        # Build a conservative CSP value from settings with fallbacks
        default_src = "'self'"
        script_src = "'self'"
        style_src = "'self'"

        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            default_src = ' '.join(settings.CSP_DEFAULT_SRC)
        if hasattr(settings, 'CSP_SCRIPT_SRC'):
            script_src = ' '.join(settings.CSP_SCRIPT_SRC)
        if hasattr(settings, 'CSP_STYLE_SRC'):
            style_src = ' '.join(settings.CSP_STYLE_SRC)

        csp_value = f"default-src {default_src}; script-src {script_src}; style-src {style_src}"
        response['Content-Security-Policy'] = csp_value
        return response
