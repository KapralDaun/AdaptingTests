from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Subject, Session, Answer, Question


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    list_display_links = ('id', 'title', 'author')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ('title',)}


class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'date', 'mark')
    list_display_links = ('id', 'user', 'subject')
    search_fields = ('user',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'description', 'level')
    list_display_links = ('id', 'subject', 'description', 'level')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'description')
    list_display_links = ('id', 'question', 'description')


admin.site.register(User, UserAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
