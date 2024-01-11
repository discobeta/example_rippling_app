from app.models import RipplingGroup, RipplingEmployee, RipplingCompany
from django.contrib import admin


class RipplingCompanyAdmin(admin.ModelAdmin):
	list_display = ['id', 'created_at', 'updated_at', 'is_access_token_valid']
	read_only_fields = ['created_at', 'updated_at']
	pass

	def is_access_token_valid(self, obj):
		return obj.is_access_token_valid()
admin.site.register(RipplingCompany, RipplingCompanyAdmin)

class RipplingEmployeeAdmin(admin.ModelAdmin):
	list_display = ['id', 'company',  'name', 'email', 'created_at', 'updated_at']
	read_only_fields = ['created_at', 'updated_at']
	pass
admin.site.register(RipplingEmployee, RipplingEmployeeAdmin)

class RipplingGroupAdmin(admin.ModelAdmin):
	list_display = ['id', 'company', 'name', 'created_at', 'updated_at']
	read_only_fields = ['created_at', 'updated_at']
	pass
admin.site.register(RipplingGroup, RipplingGroupAdmin)