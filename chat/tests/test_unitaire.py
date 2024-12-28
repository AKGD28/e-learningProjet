from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Classe  # Assurez-vous que ce chemin est correct
from chat.models import Salon, Message  # Adaptez le chemin en fonction de votre application


class TestSalonModel(TestCase):
    """Tests pour le modèle Salon."""

    def setUp(self):
        """Préparation des données pour les tests."""
        self.classe = Classe.objects.create(nom="Classe A")

    def test_salon_creation_signal(self):
        """Test que la création d'une Classe déclenche automatiquement la création d'un Salon."""
        salon = Salon.objects.get(classe=self.classe)
        self.assertIsNotNone(salon)
        self.assertEqual(salon.classe, self.classe)

    def test_default_values(self):
        """Test que les valeurs par défaut de Salon sont correctes."""
        salon = Salon.objects.get(classe=self.classe)
        self.assertTrue(salon.status)
        self.assertIsNotNone(salon.date_add)
        self.assertIsNotNone(salon.date_upd)

    def test_str_representation(self):
        """Test de la représentation en chaîne de Salon."""
        salon = Salon.objects.get(classe=self.classe)
        salon.nom = "Salon Test"
        salon.save()
        self.assertEqual(str(salon), "Salon Test")

    def test_cascade_deletion(self):
        """Test que la suppression d'une Classe supprime le Salon associé."""
        self.classe.delete()
        self.assertFalse(Salon.objects.filter(classe=self.classe).exists())


class TestMessageModel(TestCase):
    """Tests pour le modèle Message."""

    def setUp(self):
        """Préparation des données pour les tests."""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.classe = Classe.objects.create(nom="Classe B")
        self.salon = Salon.objects.create(classe=self.classe, nom="Salon Classe B")

    def test_message_creation(self):
        """Test de la création d'un message avec un utilisateur et un salon valides."""
        message = Message.objects.create(auteur=self.user, salon=self.salon, message="Hello!")
        self.assertEqual(message.auteur, self.user)
        self.assertEqual(message.salon, self.salon)
        self.assertEqual(message.message, "Hello!")

    def test_default_values(self):
        """Test que les valeurs par défaut de Message sont correctes."""
        message = Message.objects.create(auteur=self.user, salon=self.salon, message="Test Message")
        self.assertTrue(message.status)
        self.assertIsNotNone(message.date_add)
        self.assertIsNotNone(message.date_update)

    def test_str_representation(self):
        """Test de la représentation en chaîne de Message."""
        message = Message.objects.create(auteur=self.user, salon=self.salon, message="Hello!")
        self.assertEqual(str(message), "testuser")

    def test_cascade_deletion_salon(self):
        """Test que la suppression d'un Salon supprime les Messages associés."""
        message = Message.objects.create(auteur=self.user, salon=self.salon, message="Hello!")
        self.salon.delete()
        self.assertFalse(Message.objects.filter(id=message.id).exists())

    def test_cascade_deletion_user(self):
        """Test que la suppression d'un utilisateur supprime les Messages associés."""
        message = Message.objects.create(auteur=self.user, salon=self.salon, message="Hello!")
        self.user.delete()
        self.assertFalse(Message.objects.filter(id=message.id).exists())
