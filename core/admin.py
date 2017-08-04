from django.contrib import admin
from core.models import Work, Category, CommType, Tag, Comm


admin.site.register(Work)
admin.site.register(Category)
admin.site.register(CommType)
admin.site.register(Tag)
admin.site.register(Comm)