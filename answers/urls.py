from django.urls import re_path, path
from answers.views import AnswerView, AskView, InputData

urlpatterns = [
    re_path(r'answers/', AnswerView.as_view()),
    re_path(r'ask/', AskView.as_view()),
    path('input_data/', InputData.as_view()),
]
