from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import Cours
from forum.models import Sujet, Reponse


class TestForumIntegration(TestCase):
    """Tests d'intégration pour le module Forum."""

    def setUp(self):
        """Prépare les données nécessaires pour les tests."""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cours = Cours.objects.create(titre="Cours de Test")
        self.client.login(username="testuser", password="password")  # Connexion utilisateur

    # Tests pour Sujet
    def test_create_valid_sujet(self):
        """Création d'un sujet valide via POST."""
        data = {
            "titre": "Sujet Intégration",
            "question": "Question d'intégration.",
            "cours": self.cours.id,
        }
        response = self.client.post(reverse("forum-add-sujet"), data)
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertTrue(Sujet.objects.filter(titre="Sujet Intégration").exists())

    def test_create_invalid_sujet(self):
        """Création d'un sujet invalide (titre manquant)."""
        data = {
            "question": "Question sans titre.",
            "cours": self.cours.id,
        }
        response = self.client.post(reverse("forum-add-sujet"), data)
        self.assertEqual(response.status_code, 400)  # Mauvaise requête
        self.assertFalse(Sujet.objects.filter(question="Question sans titre.").exists())

    def test_fetch_sujets_for_cours(self):
        """Récupération des sujets actifs pour un cours donné."""
        Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Sujet Actif",
            question="Question active.",
            status=True,
        )
        Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Sujet Inactif",
            question="Question inactive.",
            status=False,
        )
        response = self.client.get(reverse("forum"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sujet Actif")
        self.assertNotContains(response, "Sujet Inactif")

    def test_delete_sujet_with_responses(self):
        """Suppression d'un sujet avec des réponses associées."""
        sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Sujet à supprimer",
            question="Question pour suppression.",
        )
        Reponse.objects.create(
            user=self.user,
            sujet=sujet,
            reponse="Réponse associée.",
        )
        sujet.delete()
        self.assertFalse(Sujet.objects.filter(id=sujet.id).exists())
        self.assertFalse(Reponse.objects.filter(sujet=sujet).exists())

    def test_pagination_of_sujets(self):
        """Test de la pagination sur la liste des sujets."""
        for i in range(15):  # Créez 15 sujets pour tester la pagination
            Sujet.objects.create(
                user=self.user,
                cours=self.cours,
                titre=f"Sujet {i}",
                question=f"Question {i}.",
            )
        response = self.client.get(reverse("forum") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sujet 0")
        self.assertContains(response, "Sujet 9")
        self.assertNotContains(response, "Sujet 10")  # Sur une autre page

    # Tests pour Reponse
    def test_create_valid_reponse(self):
        """Création d'une réponse valide via POST."""
        sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Sujet pour réponse",
            question="Question test.",
        )
        data = {
            "reponse": "Réponse valide.",
        }
        response = self.client.post(reverse("forum-add-reponse", args=[sujet.slug]), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reponse.objects.filter(reponse="Réponse valide.").exists())

    def test_create_invalid_reponse(self):
        """Création d'une réponse invalide (champ vide)."""
        sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Sujet pour réponse invalide",
            question="Question test.",
        )
        data = {
            "reponse": "",
        }
        response = self.client.post(reverse("forum-add-reponse", args=[sujet.slug]), data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Reponse.objects.filter(sujet=sujet).exists())

    def test_display_sujet_with_responses(self):
        """Affichage d'un sujet avec ses réponses."""
        sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            titre="Sujet avec réponses",
            question="Question test.",
        )
        Reponse.objects.create(
            user=self.user,
            sujet=sujet,
            reponse="Première réponse.",
        )
        Reponse.objects.create(
            user=self.user,
            sujet=sujet,
            reponse="Deuxième réponse.",
        )
        response = self.client.get(reverse("forum-thread", args=[sujet.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Première réponse")
        self.assertContains(response, "Deuxième réponse")
