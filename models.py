from django.db import models

# Create your models here.
# verification/models.py
from django.db import models
from django.contrib.auth.models import User

class SignatureUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    prediction_label = models.CharField(max_length=10)  # "Real" or "Forged"
    prediction_accuracy = models.FloatField()  # Percentage accuracy
    uploaded_at = models.DateTimeField(auto_now_add=True)
