from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    """Stores each spam detection prediction."""

    SPAM = 'spam'
    HAM = 'ham'
    RESULT_CHOICES = [(SPAM, 'Spam'), (HAM, 'Ham')]

    text = models.TextField(verbose_name="Email / Message Text")
    result = models.CharField(max_length=4, choices=RESULT_CHOICES)
    confidence = models.FloatField(help_text="Confidence score (0-100%)")
    spam_probability = models.FloatField(default=0.0)
    ham_probability = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"

    def __str__(self):
        snippet = self.text[:50] + '...' if len(self.text) > 50 else self.text
        return f"[{self.result.upper()}] {snippet}"

    @property
    def is_spam(self):
        return self.result == self.SPAM

    @property
    def confidence_level(self):
        if self.confidence >= 90:
            return "Very High"
        elif self.confidence >= 75:
            return "High"
        elif self.confidence >= 60:
            return "Medium"
        else:
            return "Low"
