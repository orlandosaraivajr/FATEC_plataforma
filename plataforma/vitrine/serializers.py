from rest_framework import serializers
from .models import VitrineModel
# from core.models import CURSO_FATEC
# from .models import TIPO_VAGA
class VitrineSerializer(serializers.ModelSerializer):
    aluno = serializers.StringRelatedField(many=False, read_only=True)
    curso = serializers.CharField(source='get_curso_display')
    tipo_vaga = serializers.CharField(source='get_tipo_vaga_display')

    class Meta:

        model = VitrineModel
        fields = ('aluno', 'descricao', 'linkedin', 'github', 'curso', 'tipo_vaga')