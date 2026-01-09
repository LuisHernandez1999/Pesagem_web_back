from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.pesagem.dto.veiculo_dto import VeiculoListDTO,CreateVeiculoDTO,VeiculoContagemTipoDTO
from apps.pesagem.service.veiculo_service import VeiculoServiceList
from apps.pesagem.exceptions.veiculo_exceptions import VeiculoException
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.pesagem.service.veiculo_service import VeiculoServiceCreate,VeiculoServiceContagem
from apps.pesagem.models import Veiculo
from apps.pesagem.exceptions.veiculo_exceptions import (
    VeiculoException,
    InvalidPayloadException
)
##### https de criacao
class VeiculoCreateApiView(GenericAPIView):
     permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
     queryset = Veiculo.objects.none()
     def post(self, request):
        try:
            dto = CreateVeiculoDTO(**request.data)
            veiculo_id = VeiculoServiceCreate.create(dto)
            return Response({"veiculo criado com sucesso id": veiculo_id}, status=201)

        except TypeError:
            return Response(
                {"detail": "Payload inválido"},
                status=422,
            )
        except VeiculoException as e:
            return Response(
                {"detail": e.detail},
                status=e.status_code,
            )
        except VeiculoException as e:
            return Response(
                {"detail": e.detail},
                status=e.status_code,
            )

#### http reponse de listagem de veiculos
class VeiculoListApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Veiculo.objects.none()
    def get(self, request):
        try:
            dto = VeiculoListDTO.from_request(request)
            veiculos = VeiculoServiceList.listar(dto)
            return Response(veiculos)
        except VeiculoException as e:
            return Response(
                {"Veiculo": e.detail},
                status=e.status_code,
            )


#### http reponse de listagem de veiculos por tipo de servico
class VeiculoContagemTipoApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Veiculo.objects.none()
    def get(self, request):
        try:
            dto = VeiculoContagemTipoDTO.from_request(request)
            data = VeiculoServiceContagem.contagem_por_tipo(dto)
            return Response(data, status=200)
        except ValueError as e:
            raise InvalidPayloadException(str(e))
        except VeiculoException as e:
            return Response(
                {"detail": e.detail},
                status=e.status_code,
            )