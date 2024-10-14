# admin.py
from django.contrib import admin
from testing_app.models import RegisterData

class RegisterDataAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_password')
    search_fields = ('user_name', 'user_email')
    list_filter = ('user_name',)

admin.site.register(RegisterData, RegisterDataAdmin)