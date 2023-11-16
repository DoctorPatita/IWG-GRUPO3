from django.contrib import admin
from organization.models import Organization, Member

# Register your models here.

admin.site.register(Organization)
admin.site.register(Member)