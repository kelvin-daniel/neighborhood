from django.contrib import admin
from .models import * 

# Register your models here.

class HealthAdmin(admin.ModelAdmin):
    filter_horizontal =['healthservices']

# Register your models here.
admin.site.register(Block)
admin.site.register(Health)
admin.site.register(Business)
admin.site.register(Authorities)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Notification)