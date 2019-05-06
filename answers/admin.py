from django.contrib import admin

from answers.models import Answers


class AnswersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Answers._meta.fields]

    class Meta:
        model = Answers


admin.site.register(Answers, AnswersAdmin)

