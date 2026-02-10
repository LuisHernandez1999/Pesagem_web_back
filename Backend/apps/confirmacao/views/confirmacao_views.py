from dataclasses import asdict
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.permissions import IsAuthenticated
from apps.confirmacao.models.confirmacao import ConfirmacaoServico
from apps.confirmacao.dto.confirmacao_dto import ConfirmacaoServicoCreateDTO, ImagemConfirmacaoCreateDTO
from apps.confirmacao.services.confirmacao_services import ConfirmacaoServicoCreateService
from apps.confirmacao.utils.confirmacao_utils  import upload_imagem_confirmacao


class ConfirmacaoServicoCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = ConfirmacaoServico.objects.none()
    def post(self, request):
        imagens_dto = []
        for img in request.FILES.getlist("imagens"):
            url = upload_imagem_confirmacao(img)
            imagens_dto.append(
                ImagemConfirmacaoCreateDTO(
                    imagem=url,
                    latitude=request.data.get("latitude"),
                    longitude=request.data.get("longitude"),
                )
            )

        dto = ConfirmacaoServicoCreateDTO(
            nome_vistoriador=request.data.get("nome_vistoriador"),
            data_servico=request.data.get("data_servico"),
            tipo_servico=request.data.get("tipo_servico"),
            imagens=imagens_dto,
        )
        result = ConfirmacaoServicoCreateService.executar(dto)
        return Response(asdict(result), status=201)