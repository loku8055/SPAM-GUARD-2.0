from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'result', 'confidence', 'confidence_level', 'created_at')
    list_filter = ('result', 'created_at')
    search_fields = ('text',)
    readonly_fields = ('created_at', 'confidence', 'spam_probability', 'ham_probability')
    ordering = ('-created_at',)

    def short_text(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    short_text.short_description = 'Text Preview'
