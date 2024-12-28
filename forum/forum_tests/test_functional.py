from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import Cours
from forum.models import Sujet, Reponse


class TestForumFunctional(TestCase):
    """Tests fonctionnels pour le module Forum."""

    def setUp(self):
        """Prépare les données pour les tests fonctionnels."""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cours = Cours.objects.create(titre="Cours de Test")
        self.sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Test Sujet",
            question="Ceci est une question de test.",
        )
        self.reponse = Reponse.objects.create(
            user=self.user,
            sujet=self.sujet,
            reponse="Ceci est une réponse de test.",
        )
        self.client.login(username="testuser", password="password")  # Connexion utilisateur

    # Tests pour Sujet
    def test_sujet_creation(self):
        """Test que le sujet est bien créé et affiché."""
        response = self.client.get(reverse("forum"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Sujet")

    def test_sujet_slug_generation(self):
        """Vérifie que le slug du sujet est bien généré."""
        self.assertTrue(self.sujet.slug.startswith("test-sujet"))

    def test_sujet_status(self):
        """Vérifie que les sujets avec status=False ne sont pas affichés."""
        self.sujet.status = False
        self.sujet.save()
        response = self.client.get(reverse("forum"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Sujet")

    def test_sujet_access_non_authenticated(self):
        """Vérifie qu'un utilisateur non connecté est redirigé."""
        self.client.logout()  # Déconnecte l'utilisateur
        response = self.client.get(reverse("forum"))
        self.assertEqual(response.status_code, 302)  # Redirection vers la page de connexion

    def test_sujet_detail_view(self):
        """Vérifie que la page de détail d'un sujet affiche correctement les informations."""
        response = self.client.get(reverse("forum-thread", args=[self.sujet.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.sujet.titre)
        self.assertContains(response, self.sujet.question)

    # Tests pour Reponse
    def test_reponse_creation(self):
        """Test que la réponse est bien créée et affichée."""
        response = self.client.get(reverse("forum-thread", args=[self.sujet.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ceci est une réponse de test.")

    def test_reponse_status(self):
        """Vérifie que les réponses avec status=False ne sont pas affichées."""
        self.reponse.status = False
        self.reponse.save()
        response = self.client.get(reverse("forum-thread", args=[self.sujet.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Ceci est une réponse de test.")

    def test_reponse_slug_generation(self):
        """Vérifie que le slug de la réponse est unique et bien généré."""
        self.assertTrue(self.reponse.slug.startswith("test-sujet"))
        self.assertTrue(len(self.reponse.slug.split("-")[-1]) == 8)  # Vérifie l'UUID

    def test_reponse_cascade_deletion(self):
        """Vérifie que la suppression d'un sujet supprime les réponses associées."""
        self.sujet.delete()
        self.assertFalse(Reponse.objects.filter(id=self.reponse.id).exists())

    def test_reponse_addition_functionality(self):
        """Vérifie que l'ajout d'une réponse fonctionne correctement."""
        data = {
            "reponse": "Nouvelle réponse ajoutée.",
        }
        response = self.client.post(reverse("forum-thread", args=[self.sujet.slug]), data)
        self.assertEqual(response.status_code, 302)  # Vérifie la redirection après ajout
        self.assertTrue(Reponse.objects.filter(reponse="Nouvelle réponse ajoutée.").exists())
