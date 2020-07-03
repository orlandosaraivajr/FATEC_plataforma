from django.contrib import admin
from .models import ConvenioModel


class ConvenioModelAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'aprovado_professor', 'observacao_professor',
                    'changed_at', 'created_at', 'documento',)
    date_hierarchy = 'created_at'
    search_fields = ('empresa', 'observacao_professor',
                     'aprovado_professor', 'changed_at', 'created_at')
    list_filter = ('empresa', 'created_at', )


admin.site.register(ConvenioModel, ConvenioModelAdmin)
