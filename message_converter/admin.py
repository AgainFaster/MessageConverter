from django.contrib import admin
from message_converter.models import ApiProject, PullProject, FtpAccessSetting, ApiAccessSetting, IncomingMessage, ConvertedMessageQueue, ApiHeader, MessageType


class ApiProjectAdmin(admin.ModelAdmin):
    pass


class PullProjectAdmin(admin.ModelAdmin):
    pass


class FtpAccessSettingAdmin(admin.ModelAdmin):
    pass


class ApiHeaderInline(admin.StackedInline):
    model = ApiHeader


class ApiAccessSettingAdmin(admin.ModelAdmin):
    inlines = [ApiHeaderInline,]


class IncomingMessageAdmin(admin.ModelAdmin):
    pass


class ConvertedMessageQueueAdmin(admin.ModelAdmin):
    raw_id_fields = ["original_message"]
    readonly_fields = ["original_message"]

class MessageTypeAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(ApiProject, ApiProjectAdmin)
admin.site.register(PullProject, PullProjectAdmin)
admin.site.register(FtpAccessSetting, FtpAccessSettingAdmin)
admin.site.register(ApiAccessSetting, ApiAccessSettingAdmin)
admin.site.register(IncomingMessage, IncomingMessageAdmin)
admin.site.register(ConvertedMessageQueue, ConvertedMessageQueueAdmin)
admin.site.register(MessageType, MessageTypeAdmin)