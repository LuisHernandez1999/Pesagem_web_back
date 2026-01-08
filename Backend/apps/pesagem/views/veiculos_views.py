from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.pesagem.dto.veiculo_dto import VeiculoListDTO
from apps.pesagem.service.veiculo import VeiculoServiceList


class VeiculoListApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        dto = VeiculoListDTO.from_request(request)
        return Response(VeiculoServiceList.listar(dto))
