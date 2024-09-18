from django.db import models


class TextRequest(models.Model):
    text = models.CharField(max_length=255)  # Поле для хранения текста запроса
    timestamp = models.DateTimeField(auto_now_add=True)  # Время запроса

    def __str__(self):
        return f"Request: {self.text} at {self.timestamp}"
