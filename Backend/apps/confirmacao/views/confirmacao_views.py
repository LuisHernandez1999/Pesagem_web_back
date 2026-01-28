from dataclasses import asdict
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.permissions import IsAuthenticated
from apps.confirmacao.models.confirmacao import ConfirmacaoServico
from apps.confirmacao.dto.confirmacao_dto import ConfirmacaoServicoCreateDTO, ImagemConfirmacaoCreateDTO
from apps.confirmacao.services.confirmacao_services import ConfirmacaoServicoCreateService


class ConfirmacaoServicoCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = ConfirmacaoServico.objects.none()
    def post(self, request):
        imagens_dto = [
            ImagemConfirmacaoCreateDTO(
                imagem=img.get("imagem"),
                latitude=img.get("latitude"),
                longitude=img.get("longitude"),
            )
            for img in request.data.get("imagens", [])
        ]
        dto = ConfirmacaoServicoCreateDTO(
            nome_vistoriador=request.data.get("nome_vistoriador"),
            data_servico=request.data.get("data_servico"),
            tipo_servico=request.data.get("tipo_servico"),
            imagens=imagens_dto,
        )
        result = ConfirmacaoServicoCreateService.executar(dto)
        return Response(asdict(result))
