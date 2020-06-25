from django.contrib import admin
from .models import ConvenioModel


class ConvenioModelAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'documento', 'observacao_professor',
                    'aprovado_professor', 'created_at')
    date_hierarchy = 'created_at'
    search_fields = ('empresa', 'observacao_professor',
                     'aprovado_professor', 'created_at')
    list_filter = ('empresa', 'observacao_professor',
                   'created_at', )


admin.site.register(ConvenioModel, ConvenioModelAdmin)
