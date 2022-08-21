from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .models import User, Subject, Session, Question, Answer
from .services import *
from .forms import *


def index(request):
    """
    Функция для отображения домашней страницы сайта
    """

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_visits': num_visits}
    )


def pageNotFound(request, expection):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class SubjectListView(generic.ListView):
    model = Subject
    context_object_name = 'my_subject_list'
    # queryset = Subject.objects.filter(title__icontains='test')
    template_name = 'subject_list.html'

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(SubjectListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context


def show_subject(request, subject_slug):
    subject = get_object_or_404(Subject, slug=subject_slug)

    context = {
        'subject': subject,
        'title': subject.title,
        'slug': subject_slug
    }

    return render(request, 'subject_detail.html', context=context)


def GetQuestion(request, subject_slug, question_pk, session_pk):
    session = Session.objects.get(pk=session_pk)

    if session.isFirstQuestion == 1:
        session.isFirstQuestion = 0
        session.countOfQuestions += 1
        session.save(update_fields=['isFirstQuestion', 'countOfQuestions'])
        list_answered_questions = []

        next_question = get_question(list_answered_questions, session.currentLevel, subject_slug)
        list_answered_questions.append(next_question.pk)
        session.answered_question = " ".join(map(str, list_answered_questions))
        session.save(update_fields=['answered_question'])
        next_answers = get_answers(next_question)
        form = SelectAnswer(next_answers)

    if request.method == 'POST':
        previous_question = Question.objects.get(pk=question_pk)
        previous_answers = get_answers(previous_question)

        choosen_answer = int(request.POST['is_Selected'])
        for i in previous_answers:
            if i[0] == choosen_answer:
                choosen_answer = i[1]
        check_answer = Answer.objects.get(description=choosen_answer, question=previous_question)

        if check_answer.IsTrue:
            if session.true_answer():
                return HttpResponseRedirect(reverse('testing:end_session', args=(session.pk,)))
        else:
            if session.false_answer():
                return HttpResponseRedirect(reverse('testing:end_session', args=(session.pk,)))
        session.countOfQuestions += 1
        session.save(update_fields=['countOfQuestions'])
        list_answered_questions = session.answered_question.split(",")
        print(session.answered_question)
        print(list_answered_questions)
        next_question = get_question(list_answered_questions, session.currentLevel, subject_slug)
        if next_question is None:
            return HttpResponseRedirect(reverse('testing:end_session', args=(session.pk,)))
        list_answered_questions.append(next_question.pk)
        session.answered_question = ",".join(map(str, list_answered_questions))
        session.save(update_fields=['answered_question'])
        next_answers = get_answers(next_question)
        form = SelectAnswer(next_answers)
    return render(
        request,
        "question_template.html",
        {'next_question': next_question,
         'slug': subject_slug,
         'question_pk': next_question.pk,
         'session_pk': session_pk,
         'select_answer_form': form,
         'countOfQuestions': session.countOfQuestions,
         'level': session.currentLevel
         }
    )


def StartSession(request, subject_slug):
    if request.method == 'POST':
        test = Subject.objects.get(slug=subject_slug)
        session = Session.objects.create(user=request.user, subject=test)
        question = Question.objects.filter(level=2, subject=test).first()
        return HttpResponseRedirect(reverse('testing:question', args=(test.slug, question.pk, session.pk)))
        # return HttpResponseRedirect(reverse('testing:question', args=(test.slug, question.pk, session.pk)))


def EndSession(request, session_pk):
    session = Session.objects.get(pk=session_pk)
    countOfFalseAnswers = session.countOfQuestions - session.countOfTrueAnswers
    max_value = max(session.PH_1, session.PH_2, session.PH_3, session.PH_4)
    if max_value == session.PH_1:
        session.mark = 2
    elif max_value == session.PH_2:
        session.mark = 3
    elif max_value == session.PH_3:
        session.mark = 4
    elif max_value == session.PH_4:
        session.mark = 5
    session.save()
    return render(request,
                  'end_session.html',
                  {'mark': session.mark,
                   'countOfQuestions': session.countOfQuestions,
                   'countOfTrueAnswers': session.countOfTrueAnswers,
                   'countOfFalseAnswers': countOfFalseAnswers,
                   'subject_title': session.subject
                   })


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(RegisterUser, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('testing:subjects')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(LoginUser, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('testing:subjects')


def logout_user(request):
    logout(request)
    return redirect('testing:login')