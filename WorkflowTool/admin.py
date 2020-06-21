from django.contrib import admin
from .models import GPUser, Ticket, Onboarding, TaskVsWFID, SLA, ProductRequisition, TaskVsRole, KAMTable, Item

# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    search_fields = ["WFID", "corporate_name"]

class SLAAdmin(admin.ModelAdmin):
    search_fields = ["wfid"]

class OnboardingAdmin(admin.ModelAdmin):
    search_fields = ["corporate_name"]

admin.site.register(GPUser)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Onboarding, OnboardingAdmin)
admin.site.register(TaskVsWFID)
admin.site.register(SLA, SLAAdmin)
admin.site.register(TaskVsRole)
admin.site.register(ProductRequisition)
admin.site.register(KAMTable)
admin.site.register(Item)