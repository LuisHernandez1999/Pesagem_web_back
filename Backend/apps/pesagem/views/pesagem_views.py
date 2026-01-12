from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.pesagem.dto.pesagem_dto import PesagemListDTO
from apps.pesagem.service.pesagem_service import PesagemServiceList
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.pesagem.dto.pesagem_dto import CreatePesagemDTO
from apps.pesagem.service.pesagem_service import PesagemServiceCreate,PesagemServiceListTipo, PesagemServiceList
from apps.pesagem.exceptions.pesagem_execptions import PesagemException
from apps.pesagem.models.pesagem import Pesagem
from rest_framework import status

class PesagemCreateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()

    def post(self, request):
        try:
            dto = CreatePesagemDTO(**request.data)
            pesagem_id = PesagemServiceCreate.create(dto)

            return Response(
                {"pesagem_criada_com_sucesso": pesagem_id},
                status=201
            )

        except PesagemException as e:
            return Response(
                {"detail": e.detail},
                status=e.status_code
            )

class PesagemListApiView(APIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.all()

    def get(self, request):
        dto = PesagemListDTO.from_request(request)
        data = PesagemServiceList.listar(dto)
        return Response(data, status=200)


class PesagemTipoServicoView(APIView):
    def get(self, request):
        try:
            total_seletiva = PesagemServiceListTipo.total_seletiva()
            total_cata_treco = PesagemServiceListTipo.total_cata_treco()

            return Response(
                {
                    "SELETIVA": total_seletiva,
                    "CATA_TRECO": total_cata_treco,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )