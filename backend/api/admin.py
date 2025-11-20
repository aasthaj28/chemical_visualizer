from django.contrib import admin
from .models import UploadedDataset


@admin.register(UploadedDataset)
class UploadedDatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uploaded_at')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('user__username',)

