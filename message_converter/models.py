from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class MessageType(models.Model):
    name = models.CharField(max_length=100)
    type_code = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Message Type"

    def __str__(self):
        return '%s (%s)' % (self.name, self.format)


class ApiAccessSetting(models.Model):
    host = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "API Connection"

    def __str__(self):
        return "%s (%s)" % (self.nickname, self.host) or self.host


class ApiHeader(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    setting = models.ForeignKey(ApiAccessSetting)

    class Meta:
        verbose_name = "API Header"

    def __str__(self):
        return "%s: %s" % (self.name, self.value)


class FtpAccessSetting(models.Model):
    host = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    path = models.TextField(blank=True, null=True)
    processed_path = models.TextField(blank=True, null=True, help_text="This is the path where files will be moved to after they are processed. It will be ignored if delete_processed=True.")
    delete_processed = models.BooleanField(default=False, help_text="This will delete files after they are processed rather than moving them to the processed_path.")

    class Meta:
        verbose_name = "FTP Connection"

    def __str__(self):
        return self.host + self.path


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[RegexValidator('^[\w-]+$', u'Enter only alphanumeric, dash, or underscore.', 'invalid')])
    description = models.TextField(blank=True, null=True)
    enabled = models.BooleanField(default=True)

    from_type = models.ForeignKey(MessageType, related_name="from_type_projects")
    to_type = models.ForeignKey(MessageType, related_name="to_type_projects")

    conversion_parameters = models.TextField(blank=True, null=True, help_text="JSON parameters")

    send_to_ftp = models.ForeignKey(FtpAccessSetting, related_name='send_to_ftp_projects', null=True, blank=True, help_text="An FTP destination to deliver the converted messages.")
    send_to_api = models.ForeignKey(ApiAccessSetting, related_name='send_to_api_projects', null=True, blank=True, help_text="An API destination to deliver the converted messages.")

    delivery_frequency = models.IntegerField(
        help_text="How often to deliver converted messages (in minutes). Use 0 for immediate. Minimum is the frequency of the deliver_messages periodic task.")

    delivery_message_age = models.IntegerField(
        help_text="How old a message has to be (in minutes) before it can be delivered. Use 0 for immediate.", default=0)

    messages_per_delivery = models.IntegerField(
        help_text="Maximum number of messages to send in one delivery call.", default=0)

    def __str__(self):
        return self.name

# Internet -> MessageConverter -> FTP/API
# Accept incoming messages as a POST Request, convert them if necessary, and send them off to an API/FTP somewhere else
class ApiProject(Project):

    class Meta:
        verbose_name = "API Project"

    def __str__(self):
        return self.name


# FTP -> MessageConverter -> Internet
# Push
# Occasionally poll FTP/API for new files, convert them if necessary, and send them off to an API/FTP somewhere else
class PullProject(Project):
    pull_from_ftp = models.ForeignKey(FtpAccessSetting, null=True, blank=True, help_text="Pull from an FTP endpoint. Leave blank if pulling from an API instead.")
    pull_from_api = models.ForeignKey(ApiAccessSetting, null=True, blank=True, help_text="Pull from an API endpoint. Leave blank if pulling from an FTP instead.")

    pull_frequency = models.IntegerField(
        help_text="How often to pull new messages (in minutes). Minimum is the frequency of the pull_messages periodic task.")

    check_file_size_interval = models.IntegerField(default=0,
        help_text="How often to check on a file size (in seconds) to determine if the file is done being written to. 0 won't check.")

    max_file_size_wait_time = models.IntegerField(default=5*60,
        help_text="Max time to wait for a file to be done being written to (in seconds). Default is 5 minutes.")

    class Meta:
        verbose_name = "Pull Project"

    def __str__(self):
        return self.name


class IncomingMessage(models.Model):
    message = models.TextField()
    project = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Incoming Message"
        
    def __str__(self):
        return '%s - %s' % (self.project, self.created)


# Create your models here.
class ConvertedMessageQueue(models.Model):
    original_message = models.ForeignKey(IncomingMessage, on_delete=models.SET_NULL, null=True)
    converted_message = models.TextField()
    project = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Converted Message"

    def __str__(self):
        return '%s - %s' % (self.project, self.created)


class LastDelivery(models.Model):
    project = models.OneToOneField(Project)
    last_delivered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.project, self.last_delivered)

class LastPull(models.Model):
    pull_project = models.OneToOneField(PullProject)
    last_pulled = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.pull_project, self.last_pulled)

