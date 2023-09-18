from django.contrib import admin
from .models import PolicyHolder, InsuranceModel, EventModel

admin.site.register(PolicyHolder)
admin.site.register(InsuranceModel)
admin.site.register(EventModel)