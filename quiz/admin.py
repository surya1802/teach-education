# Register your models here.

from django.contrib import admin
from .models import Subject, Question, Attempt
from django.contrib import admin

# Change "View site" link in Django admin
admin.site.site_url = "http://127.0.0.1:3000/"

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_text','subject','qtype','difficulty')
    list_filter = ('qtype','difficulty','subject')
    search_fields = ('text',)

    def short_text(self, obj):
        return obj.text[:60]
    short_text.short_description = 'Question'

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user','subject','score','started_at','finished_at')
    list_filter = ('subject',)
    search_fields = ('user__username',)
