from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.os.services.os_services import OrdemServicoService
from apps.os.dto.os_dto import OrdemServicoCreateDTO


class OrdemServicoCreateAPIView(APIView):

    CAMPOS_PERMITIDOS = {
        "pa",
        "os_numero",
        "veiculo_prefixo",
        "inicio_problema",
        "conclusao"
    }

    def post(self, request):

        extras = set(request.data.keys()) - self.CAMPOS_PERMITIDOS
        if extras:
            return Response(
                {"erro": f"Campos não permitidos: {list(extras)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            dto = OrdemServicoCreateDTO(
                pa=request.data["pa"],
                os_numero=request.data["os_numero"],
                veiculo_prefixo=request.data["veiculo_prefixo"],
                inicio_problema=request.data["inicio_problema"],
                conclusao=request.data.get("conclusao")
            )

            os = OrdemServicoService.criar(dto)

            return Response(
                {
                    "id": os.id,
                    "pa": os.pa,
                    "os_numero": os.os_numero,
                    "veiculo_prefixo": os.veiculo.prefixo,
                    "veiculo_id": os.veiculo_id,  
                    "inicio_problema": os.inicio_problema,
                    "conclusao": os.conclusao,
                    "created_at": os.created_at
                },
                status=status.HTTP_201_CREATED
            )

        except KeyError as e:
            return Response(
                {"erro": f"Campo obrigatório ausente: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
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
