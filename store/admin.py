from django.contrib import admin
from store import models
# Register your models here.

admin.site.register(models.StoreCollection)
admin.site.register(models.StoreArtifact)
admin.site.register(models.ServiceStoreIntegration)
