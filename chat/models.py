from django.db import models
from school import models as school_models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Salon(models.Model):
    """Model definition for Salon."""

    nom = models.CharField(max_length=250, null=True)
    classe = models.OneToOneField(school_models.Classe, on_delete=models.CASCADE, related_name="class_room", null=True)
    date_add = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_upd =models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.BooleanField(default=True)

    @receiver(post_save, sender=school_models.Classe)
    def create_salon(sender, instance, created, **kwargs):
        if created:
            Salon.objects.create(classe=instance)

    @receiver(post_save, sender=school_models.Classe)
    def save_salon(sender, instance, created, **kwargs):
        instance.class_room.save()

    class Meta:
        """Meta definition for Salon."""

        verbose_name = 'Salon'
        verbose_name_plural = 'Salons'

    def __str__(self):
        """Unicode representation of Salon."""
        return self.nom

class Message(models.Model):
    """Model definition for Message."""
    auteur = models.ForeignKey(User, related_name="auteur_message", on_delete=models.CASCADE)
    message = models.TextField()
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="salon")
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateField( auto_now=True)

    class Meta:
        """Meta definition for Message."""

        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        """Unicode representation of Message."""
        return self.auteur.username