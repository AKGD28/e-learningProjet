# instructor/models.py

from django.db import models
from django.contrib.auth.models import User
from school.models import Classe
from django.utils.text import slugify
import uuid

class Instructor(models.Model):
    user = models.OneToOneField(User, related_name='instructor', on_delete=models.CASCADE)
    contact = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    classe = models.ForeignKey(Classe, related_name='instructors', on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='images/instructors/', null=True, blank=True)
    bio = models.TextField(default="Votre bio")
    ville = models.CharField(max_length=255, default="Abobo")
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='instructors/photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_id = uuid.uuid4().hex[:6]
            self.slug = f"{slugify(self.user.username)}-{unique_id}"
        super(Instructor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def __str__(self):
        return self.user.username

    @property
    def get_u_type(self):
        try:
            return hasattr(self.user, 'instructor')
        except:
            return False
