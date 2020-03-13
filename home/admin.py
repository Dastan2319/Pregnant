from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Topic)
admin.site.register(models.Feedback)
admin.site.register(models.Comments)
admin.site.register(models.Preparation)
admin.site.register(models.User)
admin.site.register(models.NeededItems)
admin.site.register(models.News)
admin.site.register(models.MaternityHospital)
admin.site.register(models.roles)
admin.site.register(models.user_roles)
