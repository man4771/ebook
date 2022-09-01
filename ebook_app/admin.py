from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_title = 'eBook House'
admin.site.site_header = 'eBook House'

mymodels = (UserRole,Master,Profile,Category,Book)
for model in mymodels:
    admin.site.register(model)

