from rest_framework.generics import GenericAPIView
from dataclasses import asdict
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.os.services.os_services import OrdemServicoVisualizacaoService
from apps.os.dto.os_dto import OrdemServicoCreateDTO,OrdemServicoListFilterDTO
from apps.os.models.os import OrdemServico
from apps.os.services.os_services import OrdemServicoServiceCreate

###### POST
class OrdemServicoCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = OrdemServico.objects.none()
    def post(self, request):
        try:
            dto = OrdemServicoCreateDTO(**request.data)
            result_dto = OrdemServicoServiceCreate.create(dto)

            return Response(
                asdict(result_dto),   
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {"detail": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        


###### GET
class OrdemServicoVisualizacaoAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = OrdemServico.objects.none()
    def get(self, request):
        filtros_dto = OrdemServicoListFilterDTO(
            cursor_id=int(request.query_params.get("cursor_id"))
            if request.query_params.get("cursor_id") else None,
            veiculo_prefixo=request.query_params.get("veiculo_prefixo"),
            os_numero=request.query_params.get("os_numero"),
            pa=request.query_params.get("pa"),
            aberta=(
                request.query_params.get("aberta").lower() == "true"
                if request.query_params.get("aberta") is not None
                else None
            )
        )

        response_dto = OrdemServicoVisualizacaoService.listar(filtros_dto)

        return Response(
            asdict(response_dto),
            status=status.HTTP_200_OK
        )