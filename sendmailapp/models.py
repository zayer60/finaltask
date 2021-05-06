from django.db import models
from django.urls import reverse


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group-details', args=[str(self.id)])




class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', 'MALE'),
        ('female', 'FEMALE'),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default='male')
    dob = models.DateField()
    email = models.EmailField()
    groups = models.ManyToManyField(Group,through='PatientGroup',blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
       return reverse('patient-list')




class PatientGroup(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

