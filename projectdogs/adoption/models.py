from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse



# Create your models here.

class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    description = models.TextField()
    location = models.CharField(max_length=100, default='unknown')    
    photo = models.ImageField(upload_to='dog_photos/', default='default.jpg')
    is_adopted = models.BooleanField(default=False)
    adoption_date = models.DateField(null=True, blank=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('adoption-detail',kwargs={'pk':self.pk})


class AdoptionApplication(models.Model):
    PET_STATUS = (
        ('p', 'Pending'),
        ('a', 'Approved'),
        ('r', 'Rejected'),
    )

    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=100)
    applicant_phone_number = models.CharField(max_length=15)
    applicant_email = models.EmailField()
    vet_name = models.CharField(max_length=100)
    vet_phone_number = models.CharField(max_length=15)
    reason = models.TextField()
    application_date = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=1, choices=PET_STATUS, default='p')
    
    def __str__(self):
        return f'{self.pet_id.name} - {self.applicant.username}'

    def get_absolute_url(self):
        return reverse('adoption-detail', kwargs={'pk': self.pk})