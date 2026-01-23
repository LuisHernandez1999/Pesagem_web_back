from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.movimentacao.services.movimentacao_services import MovimentacaoServiceCreate,MovimentacaoListService
from apps.movimentacao.dto.movimentacao_dto import MovimentacaoCreateDTO,MovimentacaoListCursorDTO
from apps.movimentacao.models.movimentacao import Movimentacao

######### POST
class MovimentacaoCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Movimentacao.objects.none()
    def post(self, request):
        try:
            dto = MovimentacaoCreateDTO(**request.data)
            movimentacao = MovimentacaoServiceCreate.create(dto)
            return Response(
                {
                    "os_id": movimentacao.os_id,
                    "data_hora": movimentacao.data_hora.isoformat(),
                    "status": movimentacao.status,
                    "responsavel_id": movimentacao.responsavel_id,
                    "observacao": movimentacao.observacao,
                },
                status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response(
                {"error": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )





##### GET
class MovimentacaoListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Movimentacao.objects.none()

    def get(self, request):
        dto = MovimentacaoListCursorDTO(
            pa=request.query_params.get("pa"),
            data=request.query_params.get("data"),
            data_inicio=request.query_params.get("data_inicio"),
            data_fim=request.query_params.get("data_fim"),
            os_id=request.query_params.get("os_id"),
            os_numero=request.query_params.get("os_numero"),
            status=request.query_params.get("status"),
            responsavel_matricula=request.query_params.get("responsavel_matricula"),
            responsavel_nome=request.query_params.get("responsavel_nome"),
            veiculo_prefixo=request.query_params.get("veiculo_prefixo"),
            observacao=request.query_params.get("observacao"),
            next_cursor=request.query_params.get("next_cursor"),
            limit=int(request.query_params.get("limit", 20)),
        )

        lista, next_cursor = MovimentacaoListService.listar_com_cursor(dto)

        return Response(
            {
                "results": [item.__dict__ for item in lista],
                "next_cursor": next_cursor
            },
            status=status.HTTP_200_OK
        )