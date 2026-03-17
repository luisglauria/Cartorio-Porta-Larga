from rest_framework import serializers
from agendamento.models import Agendamento, Servico
from django.contrib.auth.models import User


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'duracao_minutos', 'preco']


class AgendamentoSerializer(serializers.ModelSerializer):
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    usuario_nome = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Agendamento
        fields = [
            'id', 'servico', 'servico_nome', 'usuario_nome',
            'data', 'hora', 'status', 'status_display',
            'observacoes', 'criado_em',
        ]
        read_only_fields = ['status', 'criado_em']

    def get_usuario_nome(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username

    def validate_data(self, value):
        from django.utils import timezone
        if value <= timezone.localdate():
            raise serializers.ValidationError('A data deve ser futura.')
        if value.weekday() >= 5:
            raise serializers.ValidationError('Atendemos apenas de segunda a sexta-feira.')
        return value

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class UsuarioSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(source='perfil.cpf', read_only=True)
    telefone = serializers.CharField(source='perfil.telefone', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'cpf', 'telefone']
