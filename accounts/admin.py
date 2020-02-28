from django.contrib import admin
from .models import CustomUser, Sickness, MedicalInformation


admin.site.register(CustomUser)
admin.site.register(Sickness)
admin.site.register(MedicalInformation)