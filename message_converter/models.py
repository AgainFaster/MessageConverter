from django.db import models

class MessageType(models.Model):
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.type

class IncomingMessage(models.Model):
    message = models.TextField()
    type = models.ForeignKey(MessageType)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.type, self.created)

# Create your models here.
class ConvertedMessageQueue(models.Model):
    original_message = models.ForeignKey(IncomingMessage, on_delete=models.SET_NULL, null=True)
    converted_message = models.TextField()
    type = models.ForeignKey(MessageType)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.type, self.created)


