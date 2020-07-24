"""
Descr: main module to operate log parsing
@author: corvit
Created: Fri Jul 24 2020 11:05 MSK
"""
# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from data.models import *


#Add user
user = User(name="corvit", email="corvit@mail.ru")
user.save()

# Application logic
first_user = User.objects.all()[0]

print(first_user.name)
print(first_user.email)
