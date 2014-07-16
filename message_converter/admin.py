from django.contrib import admin
from message_converter.models import ApiProject, PullProject, FtpAccessSetting, ApiAccessSetting, IncomingMessage, ConvertedMessageQueue


class ApiProjectAdmin(admin.ModelAdmin):
    pass


class PullProjectAdmin(admin.ModelAdmin):
    pass


class FtpAccessSettingAdmin(admin.ModelAdmin):
    pass


class ApiAccessSettingAdmin(admin.ModelAdmin):
    pass


class IncomingMessageAdmin(admin.ModelAdmin):
    pass


class ConvertedMessageQueueAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(ApiProject, ApiProjectAdmin)
admin.site.register(PullProject, PullProjectAdmin)
admin.site.register(FtpAccessSetting, FtpAccessSettingAdmin)
admin.site.register(ApiAccessSetting, ApiAccessSettingAdmin)
admin.site.register(IncomingMessage, IncomingMessageAdmin)
admin.site.register(ConvertedMessageQueue, ConvertedMessageQueueAdmin)