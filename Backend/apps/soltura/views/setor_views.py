from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework import status
from apps.soltura.models.setor import Setor
from apps.soltura.dto.setor_dtos import SetorCreateDTO
from apps.soltura.services.setor_service import (
    SetorCreateService, SetorGetService, SetorUpdateService,
    SetorDeleteService, SetorListService
)

class SetorCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Setor.objects.none()
    def post(self, request):
        dto = SetorCreateDTO(**request.data)
        setor = SetorCreateService.execute(dto)
        return Response(vars(setor), status=status.HTTP_201_CREATED)

class SetorGetAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Setor.objects.none()
    def get(self, request, setor_id):
        setor = SetorGetService.execute(setor_id)
        if not setor:
            return Response({"detail": "Não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(vars(setor))

class SetorUpdateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Setor.objects.none()
    def put(self, request, setor_id):
        dto = SetorCreateDTO(**request.data)
        setor = SetorUpdateService.execute(setor_id, dto)
        if not setor:
            return Response({"detail": "Não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(vars(setor))

class SetorDeleteAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Setor.objects.none()
    def delete(self, request, setor_id):
        success = SetorDeleteService.execute(setor_id)
        if not success:
            return Response({"detail": "Não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SetorListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Setor.objects.none()
    def get(self, request):
        last_id = request.query_params.get("last_id")
        limit = int(request.query_params.get("limit", 50))
        last_id = int(last_id) if last_id else None
        setores = SetorListService.execute(last_id=last_id, limit=limit)
        return Response([vars(s) for s in setores])
