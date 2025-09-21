import sys
from pathlib import Path
import os
import django
import traceback

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

from django.test import RequestFactory
from django.urls import resolve

rf = RequestFactory()
req = rf.get('/api/books/')
match = resolve('/api/books/')
view_func = match.func

print('Resolved view:', view_func)

try:
    resp = view_func(req)
    # render if needed (e.g., TemplateResponse)
    if hasattr(resp, 'render'):
        resp.render()
    print('Response status:', resp.status_code)
    print('Response content:', getattr(resp, 'content', b'')[:500])
except Exception:
    print('Exception when calling view:')
    traceback.print_exc()
