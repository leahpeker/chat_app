from django.db import models
from datetime import date


class Conversation(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.title}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message: {self.text}"


class MessageThought(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thought: {self.text}"
