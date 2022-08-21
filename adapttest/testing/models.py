from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
import pandas as pd


class User(AbstractUser):
    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse('user-info', args=[str(self.id)])


class Subject(models.Model):
    title = models.CharField(max_length=30, verbose_name="Название курса")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Автор курса")

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('subject-detail', args=[str(self.slug)])


class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    level = models.IntegerField()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['subject']

    def __str__(self):
        """
                String for representing the Model object (in Admin site etc.)
        """
        return self.description


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    IsTrue = models.BooleanField()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['question']

    def __str__(self):
        """
                String for representing the Model object (in Admin site etc.)
        """
        return self.description


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    countOfQuestions = models.IntegerField(default=0)
    countOfTrueAnswers = models.IntegerField(default=0)
    countOfDowngradeLevel = models.IntegerField(default=0)
    countOfAnsweredLevelQuestions = models.IntegerField(default=0)
    currentLevel = models.IntegerField(default=2)
    isFirstQuestion = models.IntegerField(default=1)

    PH_1 = models.FloatField(default=0.25)
    PH_2 = models.FloatField(default=0.25)
    PH_3 = models.FloatField(default=0.25)
    PH_4 = models.FloatField(default=0.25)

    Table_level = pd.DataFrame({
        'P(A/H1)': [0.45, 0.20, 0.01, 0.001],
        'P(A/H2)': [0.65, 0.35, 0.1, 0.01],
        'P(A/H3)': [0.95, 0.9, 0.85, 0.8],
        'P(A/H4)': [0.999, 0.999, 0.95, 0.9]
    }, index=['Level1', 'Level2', 'Level3', 'Level4'])

    def true_answer(self):
        print("ПРАВИЛЬНЫЙ ОТВЕТ!")
        Sum = self.P_A()

        print(Sum)
        self.P_H_N_A(Sum, True)
        self.countOfAnsweredLevelQuestions += 1
        self.countOfTrueAnswers += 1
        self.save()
        if self.countOfAnsweredLevelQuestions == 2:
            if self.currentLevel == 4:
                self.mark = 5
                self.save()
                return True
            self.currentLevel += 1
            self.countOfAnsweredLevelQuestions = 0
        self.save()
        print(self.PH_1 + self.PH_2 + self.PH_3 + self.PH_4)
        print(self.PH_1, self.PH_2, self.PH_3, self.PH_4)
        return False

    def false_answer(self):
        print("FALSE ANSWER")

        Sum = 1 - self.P_A()
        #Sum = 1 - self.P_A()
        print("Sum:", Sum)
        self.P_H_N_A(Sum, False)

        self.countOfAnsweredLevelQuestions -= 1
        self.save()
        if self.currentLevel == 1:
            pass
        if self.countOfAnsweredLevelQuestions == -2:
            if self.currentLevel == 1:
                self.mark = 2
                self.save()
                return True
            self.currentLevel -= 1
            self.countOfDowngradeLevel += 1
            if self.countOfDowngradeLevel == 3:
                return True
            self.countOfAnsweredLevelQuestions = 0
        self.save()
        print(self.PH_1 + self.PH_2 + self.PH_3 + self.PH_4)
        print(self.PH_1, self.PH_2, self.PH_3, self.PH_4)
        return False

    def P_H_N_A(self, p_a, is_True):
        if is_True:
            if self.currentLevel == 1:
                self.PH_1 = self.Table_level.loc['Level1']['P(A/H1)'] * self.PH_1 / p_a
                self.PH_2 = self.Table_level.loc['Level1']['P(A/H2)'] * self.PH_2 / p_a
                self.PH_3 = self.Table_level.loc['Level1']['P(A/H3)'] * self.PH_3 / p_a
                self.PH_4 = self.Table_level.loc['Level1']['P(A/H4)'] * self.PH_4 / p_a
            elif self.currentLevel == 2:
                self.PH_1 = self.Table_level.loc['Level2']['P(A/H1)'] ** 2 * self.PH_1 / p_a
                self.PH_2 = self.Table_level.loc['Level2']['P(A/H2)'] ** 2 * self.PH_2 / p_a
                self.PH_3 = self.Table_level.loc['Level2']['P(A/H3)'] ** 2 * self.PH_3 / p_a
                self.PH_4 = self.Table_level.loc['Level2']['P(A/H4)'] ** 2 * self.PH_4 / p_a
            elif self.currentLevel == 3:
                self.PH_1 = self.Table_level.loc['Level3']['P(A/H1)'] ** 3 * self.PH_1 / p_a
                self.PH_2 = self.Table_level.loc['Level3']['P(A/H2)'] ** 3 * self.PH_2 / p_a
                self.PH_3 = self.Table_level.loc['Level3']['P(A/H3)'] ** 3 * self.PH_3 / p_a
                self.PH_4 = self.Table_level.loc['Level3']['P(A/H4)'] ** 3 * self.PH_4 / p_a
            elif self.currentLevel == 4:
                self.PH_1 = self.Table_level.loc['Level4']['P(A/H1)'] ** 4 * self.PH_1 / p_a
                self.PH_2 = self.Table_level.loc['Level4']['P(A/H2)'] ** 4 * self.PH_2 / p_a
                self.PH_3 = self.Table_level.loc['Level4']['P(A/H3)'] ** 4 * self.PH_3 / p_a
                self.PH_4 = self.Table_level.loc['Level4']['P(A/H4)'] ** 4 * self.PH_4 / p_a
        else:
            if self.currentLevel == 1:
                self.PH_1 = (1 - self.Table_level.loc['Level1']['P(A/H1)']) * self.PH_1 / p_a
                self.PH_2 = (1 - self.Table_level.loc['Level1']['P(A/H2)']) * self.PH_2 / p_a
                self.PH_3 = (1 - self.Table_level.loc['Level1']['P(A/H3)']) * self.PH_3 / p_a
                self.PH_4 = (1 - self.Table_level.loc['Level1']['P(A/H4)']) * self.PH_4 / p_a
            elif self.currentLevel == 2:
                self.PH_1 = (1 - self.Table_level.loc['Level2']['P(A/H1)']) ** 2 * self.PH_1 / p_a
                self.PH_2 = (1 - self.Table_level.loc['Level2']['P(A/H2)']) ** 2 * self.PH_2 / p_a
                self.PH_3 = (1 - self.Table_level.loc['Level2']['P(A/H3)']) ** 2 * self.PH_3 / p_a
                self.PH_4 = (1 - self.Table_level.loc['Level2']['P(A/H4)']) ** 2 * self.PH_4 / p_a
            elif self.currentLevel == 3:
                self.PH_1 = (1 - self.Table_level.loc['Level3']['P(A/H1)']) ** 3 * self.PH_1 / p_a
                self.PH_2 = (1 - self.Table_level.loc['Level3']['P(A/H2)']) ** 3 * self.PH_2 / p_a
                self.PH_3 = (1 - self.Table_level.loc['Level3']['P(A/H3)']) ** 3 * self.PH_3 / p_a
                self.PH_4 = (1 - self.Table_level.loc['Level3']['P(A/H4)']) ** 3 * self.PH_4 / p_a
            elif self.currentLevel == 4:
                self.PH_1 = (1 - self.Table_level.loc['Level4']['P(A/H1)']) ** 4 * self.PH_1 / p_a
                self.PH_2 = (1 - self.Table_level.loc['Level4']['P(A/H2)']) ** 4 * self.PH_2 / p_a
                self.PH_3 = (1 - self.Table_level.loc['Level4']['P(A/H3)']) ** 4 * self.PH_3 / p_a
                self.PH_4 = (1 - self.Table_level.loc['Level4']['P(A/H4)']) ** 4 * self.PH_4 / p_a

    def P_A(self):
        Sum = 0
        if self.currentLevel == 1:
            Sum = self.Table_level.loc['Level1']['P(A/H1)'] * self.PH_1 + self.Table_level.loc[
                'Level1']['P(A/H2)'] * self.PH_2 + self.Table_level.loc['Level1']['P(A/H3)'] * self.PH_3 + \
                  self.Table_level.loc['Level1']['P(A/H4)'] * self.PH_4
        elif self.currentLevel == 2:
            Sum = self.Table_level.loc['Level2']['P(A/H1)'] ** 2 * self.PH_1 + self.Table_level.loc[
                'Level2']['P(A/H2)'] ** 2 * self.PH_2 + self.Table_level.loc['Level2']['P(A/H3)'] ** 2 * self.PH_3 + \
                  self.Table_level.loc['Level2']['P(A/H4)'] ** 2 * self.PH_4
        elif self.currentLevel == 3:
            Sum = self.Table_level.loc['Level3']['P(A/H1)'] ** 3 * self.PH_1 + self.Table_level.loc[
                'Level3']['P(A/H2)'] ** 3 * self.PH_2 + self.Table_level.loc['Level3']['P(A/H3)'] ** 3 * self.PH_3 + \
                  self.Table_level.loc['Level3']['P(A/H4)'] ** 3 * self.PH_4
        elif self.currentLevel == 4:
            Sum = self.Table_level.loc['Level4']['P(A/H1)'] ** 4 * self.PH_1 + self.Table_level.loc[
                'Level4']['P(A/H2)'] ** 4 * self.PH_2 + self.Table_level.loc['Level4']['P(A/H3)'] ** 4 * self.PH_3 + \
                  self.Table_level.loc['Level4']['P(A/H4)'] ** 4 * self.PH_4
        return Sum

    date = models.DateTimeField(auto_now_add=True)
    mark = models.IntegerField(default=0)
    answered_question = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'
        ordering = ['user']

    def __str__(self):

        return str(self.user)

    def get_absolute_url(self):

        return reverse('model-detail-view', args=[str(self.id)])
