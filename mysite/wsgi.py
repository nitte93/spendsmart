"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

print("golala-wsgi")
application = get_wsgi_application()

# # Add this debug function
# async def debug_application(scope, receive, send):
#     print(f"Received request wsgi: {scope['type']} - {scope['path']}")
#     await application(scope, receive, send)

# # Replace the original application with the debug version
# application = debug_application