from django import forms
from quiz.models import StudentAnswer, Answer

class TakeQuizForm(forms.ModelForm):
    class Meta:
        model = StudentAnswer
        fields = ['answer']

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les réponses disponibles pour la question actuelle
        self.fields['answer'].queryset = Answer.objects.filter(question=question)
        self.fields['answer'].widget = forms.RadioSelect()
        self.fields['answer'].label = question.text
