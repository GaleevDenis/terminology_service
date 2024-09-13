from django.contrib import admin

from .models import Handbook, HandbookElement, HandbookVersion
# Register your models here.
admin.site.register(Handbook)
admin.site.register(HandbookElement)
admin.site.register(HandbookVersion)