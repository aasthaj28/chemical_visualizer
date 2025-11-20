"""
Database models for the API.
"""
from django.db import models
from django.contrib.auth.models import User


class UploadedDataset(models.Model):
    """Model to store uploaded dataset information."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    file_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary_json = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at}"

