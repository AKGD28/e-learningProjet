# student/models.py

from django.db import models
from django.contrib.auth.models import User
from quiz.models import Quiz, TakenQuiz
from school.models import Classe
from django.utils.text import slugify
import uuid

class Student(models.Model):
    user = models.OneToOneField(User, related_name='student_user', on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='students', null=True)
    photo = models.ImageField(upload_to='images/students/', null=True, blank=True)
    bio = models.TextField(default="Votre bio")
    ville = models.CharField(max_length=255, default="Abobo")
    score = models.IntegerField(default=0)  # Champ ajouté pour le score
    date_add = models.DateTimeField(auto_now_add=True)
    quizzes = models.ManyToManyField(Quiz, through=TakenQuiz, related_name='students')
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_id = uuid.uuid4().hex[:6]
            self.slug = f"{slugify(self.user.username)}-{unique_id}"
        super(Student, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username

    @property
    def get_u_type(self):
        try:
            user = User.objects.get(id=self.user.id)
            check = user.student_user
            return True
        except:
            return False

    def get_unanswered_questions(self, quiz):
        """
        Retourne les questions non répondues par l'étudiant pour un quiz donné.
        """
        answered_questions = self.quiz_answers.filter(answer__question__quiz=quiz).values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text').prefetch_related('answers')
        return questions
    
    def get_successful_quizzes_count(self):
        return self.quizzes.filter(takenquiz__student=self, takenquiz__percentage__gte=50).count()
