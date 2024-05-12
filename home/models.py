from django.db import models

# Create your models here.
class Aadhaar(models.Model):
    aadhaar_number = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    def __str__(self):
        return self.name
    

class Aadhaar_detail(models.Model):
    aadhaar_number = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    def __str__(self):
        return self.name