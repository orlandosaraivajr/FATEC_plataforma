from django.contrib import admin
from .models import User


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active',
                    'is_student', 'is_teacher', 'is_company', 'last_login')
    date_hierarchy = 'last_login'
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('last_login', 'is_student', 'is_teacher', 'is_company', )


admin.site.register(User, UserModelAdmin)
