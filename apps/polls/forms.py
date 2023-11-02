from django.forms import ModelForm
from .models import Question, Choice

class QuestionCreationForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class ChoiceCreationForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']