import os
import sys
from pathlib import Path
import django
from django.test import Client

# Make sure project root is on sys.path so imports work when running this script directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

client = Client()
resp = client.get('/api/books/')
print('status_code:', resp.status_code)
print('content:', resp.content.decode())
