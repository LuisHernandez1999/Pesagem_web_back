from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.colaborador.dto.colaborador_dto import CreateColaboradorDTO,ColaboradorListDTO
from apps.colaborador.services.colaborador_services import ColaboradorServiceCreate,ColaboradorServiceList
from apps.colaborador.exceptions.colaborador_exceptions import ColaboradorException
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.colaborador.models.colaborador import Colaborador

##### respotas http de criacao 
class ColaboradorCreateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Colaborador.objects.none()
    def post(self, request):
        try:
            dto = CreateColaboradorDTO(**request.data)
            colaborador_id = ColaboradorServiceCreate.create(dto)
            return Response({"colaborador criado com sucesso": colaborador_id}, status=201)
        except ColaboradorException as e:
            return Response({"detail": e.detail}, status=e.status_code)
        
#### listagem com retorno http e seus recptivos codigo de erro 
class ColaboradorListApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Colaborador.objects.all()
    def get(self, request):
        dto = ColaboradorListDTO.from_request(request)
        data = ColaboradorServiceList.listar(dto)
        return Response(data, status=200)

