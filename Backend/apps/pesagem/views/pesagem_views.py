from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.pesagem.dto.pesagem_dto import CreatePesagemDTO,PesagemListDTO,ExibirPesagemPorMesDTO 
from apps.pesagem.service.pesagem_service import PesagemServiceCreate,PesagemServiceListTipo, PesagemListService,ExibirPesagemPorMesService,PesagemTotalService
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

class PesagemListApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
    def get(self, request):
        dto = PesagemListDTO(
            start_date=request.GET.get("start_date"),
            end_date=request.GET.get("end_date"),
            prefixo=request.GET.get("prefixo"),
            motorista=request.GET.get("motorista"),
            volume_carga=request.GET.get("volume_carga"),
            cooperativa=request.GET.get("cooperativa"),
            numero_doc=request.GET.get("numero_doc"),
            responsavel_coop=request.GET.get("responsavel_coop"),
            tipo_pesagem=request.GET.get("tipo_pesagem"),
            garagem=request.GET.get("garagem"),
            turno=request.GET.get("turno"),
            limit=int(request.GET.get("limit", 20)),
            cursor_id=request.GET.get("cursor"),
        )
        result = PesagemListService.execute(dto)
        return Response(result)

   
    

class ExibirPesagemPorMesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
    def get(self, request):
        dto = ExibirPesagemPorMesDTO(
            start_date=request.GET.get("start_date"),
            end_date=request.GET.get("end_date"),
            tipo_pesagem=request.GET.get("tipo_pesagem"),
        )
        result = ExibirPesagemPorMesService.execute(dto)
        return Response(result, status=200)



class PesagemTotalAPIView(GenericAPIView):
    permission_classes=[IsAuthenticated,DjangoModelPermissionsWithView]
    queryset=Pesagem.objects.none()
    def get(self,request):
        try:
            total_pesagem= PesagemTotalService.total_pesagem()

            return Response(
                {
                    "Total_pesagem": total_pesagem
                }
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )





class PesagemTipoServicoView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
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
        

