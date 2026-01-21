# apps/os/views/os_create_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.os.services.os_services import OrdemServicoService
from apps.os.dto.os_dto  import OrdemServicoCreateDTO


class OrdemServicoCreateAPIView(APIView):
    def post(self, request):
        try:
            dto = OrdemServicoCreateDTO(
                pa=request.data.get('pa'),
                os_numero=request.data.get('os_numero'),
                veiculo_id=request.data.get('veiculo_id'),
                inicio_problema=request.data.get('inicio_problema')
            )

            os = OrdemServicoService.criar(dto)

            return Response(
                {
                    "id": os.id,
                    "os_numero": os.os_numero,
                    "veiculo": os.veiculo.prefixo,
                    "pa": os.pa,
                    "inicio_problema": os.inicio_problema,
                    "created_at": os.created_at,
                },
                status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response(
                {"erro": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"erro": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
