from dataclasses import asdict
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.response import Response
from rest_framework import status
from apps.soltura.models.rota import Rota
from apps.soltura.dto.rota_dtos import (
    RotaCreateDTO,
    RotaUpdateDTO,
    RotaListFiltroDTO,
)
from apps.soltura.services.rotas_services import (CriarRotaService,AtualizarRotaService
                                                  ,DeletarRotaService,ListarRotaService)



class RotaCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Rota.objects.none()
    def post(self, request):
        dto = RotaCreateDTO(**request.data)
        rota = CriarRotaService.executar(dto)
        return Response(rota.__dict__, status=status.HTTP_201_CREATED)


class RotaListView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    def get(self, request):
        dto = RotaListFiltroDTO(
            pa=request.query_params.get("pa"),
            tipo_servico=request.query_params.get("tipo_servico"),
            cursor=(
                int(request.query_params["cursor"])
                if "cursor" in request.query_params
                else None
            ),
            limit=int(request.query_params.get("limit", 10)),
        )
        result = ListarRotaService.executar(dto)
        return Response(asdict(result))


class RotaUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Rota.objects.none()
    def put(self, request, id_rota):
        dto = RotaUpdateDTO(id_rota=id_rota, **request.data)
        rota = AtualizarRotaService.executar(dto)
        return Response(rota.__dict__)


class RotaDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Rota.objects.none()
    def delete(self, request, id_rota):
        DeletarRotaService.executar(id_rota)
        return Response(status=status.HTTP_204_NO_CONTENT)
