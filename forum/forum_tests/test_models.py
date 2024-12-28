from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Cours  # Remplacez par le chemin correct si nécessaire
from forum.models import Sujet, Reponse  # Assurez-vous que le chemin est correct


class TestSujetModel(TestCase):
    """Tests pour le modèle Sujet."""

    def setUp(self):
        """Prépare les données pour les tests."""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cours = Cours.objects.create(titre="Cours de Test")
        self.sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Test Sujet",
            question="Ceci est une question de test."
        )

    def test_sujet_creation(self):
        """Vérifie que le Sujet est créé correctement."""
        self.assertEqual(self.sujet.user, self.user)
        self.assertEqual(self.sujet.cours, self.cours)
        self.assertEqual(self.sujet.titre, "Test Sujet")
        self.assertEqual(self.sujet.question, "Ceci est une question de test.")

    def test_slug_generation(self):
        """Vérifie que le slug est généré correctement."""
        self.sujet.save()  # Appelle la méthode `save`
        self.assertIsNotNone(self.sujet.slug)
        self.assertIn("test-sujet", self.sujet.slug)

    def test_default_values(self):
        """Vérifie les valeurs par défaut."""
        self.assertTrue(self.sujet.status)
        self.assertIsNotNone(self.sujet.date_add)
        self.assertIsNotNone(self.sujet.date_update)

    def test_str_representation(self):
        """Vérifie la représentation en chaîne de Sujet."""
        self.assertEqual(str(self.sujet), "Test Sujet")


class TestReponseModel(TestCase):
    """Tests pour le modèle Reponse."""

    def setUp(self):
        """Prépare les données pour les tests."""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cours = Cours.objects.create(titre="Cours de Test")
        self.sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Test Sujet",
            question="Ceci est une question de test."
        )
        self.reponse = Reponse.objects.create(
            user=self.user,
            sujet=self.sujet,
            reponse="Ceci est une réponse de test."
        )

    def test_reponse_creation(self):
        """Vérifie que la Réponse est créée correctement."""
        self.assertEqual(self.reponse.user, self.user)
        self.assertEqual(self.reponse.sujet, self.sujet)
        self.assertEqual(self.reponse.reponse, "Ceci est une réponse de test.")

    def test_slug_generation(self):
        """Vérifie que le slug est généré correctement."""
        self.reponse.save()  # Appelle la méthode `save`
        self.assertIsNotNone(self.reponse.slug)
        self.assertIn("test-sujet", self.reponse.slug)

    def test_default_values(self):
        """Vérifie les valeurs par défaut."""
        self.assertTrue(self.reponse.status)
        self.assertIsNotNone(self.reponse.date_add)
        self.assertIsNotNone(self.reponse.date_update)

    def test_str_representation(self):
        """Vérifie la représentation en chaîne de Reponse."""
        self.assertEqual(str(self.reponse), "Test Sujet")

    def test_cascade_deletion(self):
        """Vérifie que la suppression d'un Sujet supprime les Réponses associées."""
        self.sujet.delete()
        self.assertFalse(Reponse.objects.filter(id=self.reponse.id).exists())
