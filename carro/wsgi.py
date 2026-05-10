"""
WSGI config for carro project.
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Definir settings de produção
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carro.settings')

# Base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Aplicação WSGI
application = get_wsgi_application()

# WhiteNoise para servir ficheiros estáticos em produção
application = WhiteNoise(
    application,
    root=os.path.join(BASE_DIR, 'staticfiles'),
)

# Compressão e cache (melhor performance)
application.add_files(
    os.path.join(BASE_DIR, 'staticfiles'),
    prefix='static/'
)
