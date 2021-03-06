from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, ProjectList, Language, Skill, Education, ServiceList, Report


class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(ProjectList)
admin.site.register(Language)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(ServiceList)
admin.site.register(Report)