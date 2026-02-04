from dataclasses import asdict
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.response import Response
from rest_framework import status
from apps.celular.models.celular import Celular
from apps.celular.dto.celular_dto import (CelularCreateDTO,CelularListRequestDTO,
                                          CelularDeleteRequestDTO,CelularUpdateRequestDTO)
from apps.celular.services.celular_service import (CelularCreateService,CelularListService,
                                                   CelularDeleteService,CelularUpdateService)
from apps.celular.exceptions.celular_exceptions import CelularException



class CelularCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Celular.objects.none()
    def post(self, request):
        try:
            dto = CelularCreateDTO(
                numero=request.data.get("numero"),
                ativo=request.data.get("ativo", True),
                modelo=request.data.get("modelo"),
                fabricante=request.data.get("fabricante"),
                garagem_atual=request.data.get("garagem_atual"),
                codigo_imei=request.data.get("codigo_imei"),
                apelido=request.data.get("apelido"),
            )
            response_dto = CelularCreateService.execute(dto)
            return Response(
                asdict(response_dto),
                status=status.HTTP_201_CREATED,
            )
        except CelularException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CelularListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Celular.objects.none()
    def get(self, request, *args, **kwargs):
        request_dto = CelularListRequestDTO(
            cursor=request.query_params.get("cursor")
        )
        response_dto = CelularListService.listar_celulares(request_dto)
        return Response(
            asdict(response_dto),
            status=status.HTTP_200_OK
        )
    

class CelularDeleteAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    def delete(self, request, celular_id, *args, **kwargs):
        dto = CelularDeleteRequestDTO(celular_id=celular_id)
        response_dto = CelularDeleteService.delete(dto)
        return Response(
            asdict(response_dto),
            status=status.HTTP_200_OK
        )
    
class CelularUpdateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    def patch(self, request, celular_id, *args, **kwargs):
        dto = CelularUpdateRequestDTO(
            celular_id=celular_id,
            **request.data
        )
        response_dto = CelularUpdateService.update(dto)
        return Response(
            asdict(response_dto),
            status=status.HTTP_200_OK
        )