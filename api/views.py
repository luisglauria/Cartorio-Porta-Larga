from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from agendamento.models import Agendamento, Servico
from .serializers import AgendamentoSerializer, ServicoSerializer, UsuarioSerializer


class ServicoViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista os serviços disponíveis. Acesso público."""
    queryset = Servico.objects.filter(ativo=True)
    serializer_class = ServicoSerializer
    permission_classes = [permissions.AllowAny]


class AgendamentoViewSet(viewsets.ModelViewSet):
    """CRUD de agendamentos do usuário autenticado."""
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Agendamento.objects.all().select_related('usuario', 'servico')
        return Agendamento.objects.filter(usuario=user).select_related('servico')

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        agendamento = self.get_object()
        if not agendamento.pode_cancelar:
            return Response(
                {'detail': 'Este agendamento não pode ser cancelado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        agendamento.status = 'cancelado'
        agendamento.save()
        return Response({'detail': 'Agendamento cancelado.'})

    @action(detail=False, methods=['get'])
    def proximos(self, request):
        from django.utils import timezone
        qs = self.get_queryset().filter(
            data__gte=timezone.localdate(),
            status__in=['pendente', 'confirmado']
        ).order_by('data', 'hora')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class MeuPerfilView(viewsets.ViewSet):
    """Dados do usuário autenticado."""
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


class CustomObtainToken(ObtainAuthToken):
    """Login via API — retorna token + dados do usuário."""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'nome': user.get_full_name() or user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        })
