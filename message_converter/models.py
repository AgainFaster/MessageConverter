import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class MessageType(models.Model):
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.type


class ApiAccessSetting(models.Model):
    host = models.CharField(max_length=100, unique=True)
    user = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.host


class FtpAccessSetting(models.Model):
    host = models.CharField(max_length=100, unique=True)
    user = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, unique=True)
    path = models.TextField()

    def __str__(self):
        return self.host + self.path


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[RegexValidator('^[\w-]+$', u'Enter only alphanumeric, dash, or underscore.', 'invalid')])
    description = models.TextField(blank=True, null=True)

    from_type = models.ForeignKey(MessageType, related_name="from_type_projects")
    to_type = models.ForeignKey(MessageType, related_name="to_type_projects")

    send_to_ftp = models.ForeignKey(FtpAccessSetting, related_name='send_to_ftp_projects', null=True, blank=True, help_text="An FTP destination to deliver the converted messages.")
    send_to_api = models.ForeignKey(ApiAccessSetting, related_name='send_to_api_projects', null=True, blank=True, help_text="An API destination to deliver the converted messages.")

    delivery_frequency = models.IntegerField(
        help_text="How often to deliver converted messages (in minutes). Use 0 for immediate. Minimum is the frequency of the deliver_messages periodic task.")


class ApiProject(Project):

    def __str__(self):
        return self.name


class PullProject(Project):
    pull_from_ftp = models.ForeignKey(FtpAccessSetting, null=True, blank=True, help_text="Pull from an FTP endpoint. Leave blank if pulling from an API instead.")
    pull_from_api = models.ForeignKey(ApiAccessSetting, null=True, blank=True, help_text="Pull from an API endpoint. Leave blank if pulling from an FTP instead.")

    pull_frequency = models.IntegerField(
        help_text="How often to pull new messages (in minutes). Minimum is the frequency of the pull_messages periodic task.")

    def __str__(self):
        return self.name


class IncomingMessage(models.Model):
    message = models.TextField()
    project = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.type, self.created)


# Create your models here.
class ConvertedMessageQueue(models.Model):
    original_message = models.ForeignKey(IncomingMessage, on_delete=models.SET_NULL, null=True)
    converted_message = models.TextField()
    project = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.project, self.created)


class LastDelivery(models.Model):
    project = models.ForeignKey(Project, unique=True)
    last_delivered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.project, self.last_delivered)