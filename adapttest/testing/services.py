from .models import *
import random
from django.db.models import Q


def get_question(answered_questions, level, subject_slug):

    for i in Question.objects.filter(level=level, subject__slug=subject_slug):
        if check_questions(answered_questions, i):
            next_question = i
            return next_question


def get_answers(question):
    list_answers = []
    i_counter = 1
    for i in Answer.objects.all():
        if i.question == question:
            list_answers.append((i_counter, i))
            i_counter += 1
    return list_answers


def check_questions(answered_questions, checking_question):
    for i in answered_questions:
        answered_question = Question.objects.get(pk=i)
        if answered_question.pk == checking_question.pk:
            return False
    return True




