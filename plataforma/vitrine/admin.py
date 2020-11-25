from django.contrib import admin
from .models import VitrineModel


class VitrineModelAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'descricao', 'linkedin',
                    'github', 'curso', 'tipo_vaga','created_at',)
    date_hierarchy = 'created_at'
    search_fields = ('aluno', 'descricao','github',
                     'linkedin', 'changed_at', 'created_at')
    list_filter = ('aluno', 'created_at', )


admin.site.register(VitrineModel, VitrineModelAdmin)