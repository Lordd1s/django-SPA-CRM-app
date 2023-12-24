from django.contrib import admin
from final_course import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.CV)
admin.site.register(models.Vacancy)
admin.site.register(models.Application)
admin.site.register(models.Group)
admin.site.register(models.Message)
