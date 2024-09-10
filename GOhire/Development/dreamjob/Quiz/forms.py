from django import forms
from .models import Question

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(questions):
            self.fields[f'question_{i}'] = forms.ChoiceField(
                label=question.question_text,
                choices=[
                    (question.option1, question.option1),
                    (question.option2, question.option2),
                    (question.option3, question.option3),
                    (question.option4, question.option4)
                ],
                widget=forms.RadioSelect
            )
