from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """Tabular Inline View for Choice"""

    model = Choice
    min_num = 3
    max_num = 20
    extra = 1
    fields = ("choice_text", "votes")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin View for Question"""

    list_display = ("question_text", "pub_date", "choices_count")
    list_filter = ("pub_date",)
    inlines = [
        ChoiceInline,
    ]
    search_fields = ("question_text",)
    autocomplete_fields = ["voted_by", "created_by"]

    @admin.display(description="No. of Choices")
    def choices_count(self, obj):
        return obj.choice_set.count()
