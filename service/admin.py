from django.contrib import admin

from service.models import ServicePost, BasicPacket, StandardPacket, PremiumPacket


admin.site.register(ServicePost)
admin.site.register(BasicPacket)
admin.site.register(StandardPacket)
admin.site.register(PremiumPacket)