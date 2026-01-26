from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.insumos.dto.insumos_dto import InsumoCreateDTO
from apps.insumos.services.insumos_services import InsumoServiceCreate
from apps.insumos.dto.insumos_dto import InsumoListCursorDTO


class InsumoCreateAPIView(APIView):
    CAMPOS_PERMITIDOS = {
        "id_movimentacao",
        "item_insumo"
    }
    def post(self, request):
        extras = set(request.data.keys()) - self.CAMPOS_PERMITIDOS
        if extras:
            return Response(
                {"erro": f"Campos não permitidos: {list(extras)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            dto = InsumoCreateDTO(
                id_movimentacao=int(request.data["id_movimentacao"]),
                item_insumo=request.data["item_insumo"]
            )
            insumo = InsumoServiceCreate.criar(dto)
            return Response(
                {
                    "id_insumo": insumo.id_insumo,
                    "id_movimentacao": insumo.movimentacao_id,
                    "item_insumo": insumo.item_insumo,
                    "created_at": insumo.created_at
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




class InsumoListAPIView(APIView):
    def get(self, request):
        try:
            dto = InsumoListCursorDTO(
                id_movimentacao=int(request.query_params.get("id_movimentacao"))
                    if request.query_params.get("id_movimentacao") else None,
                next_cursor=int(request.query_params.get("next_cursor"))
                    if request.query_params.get("next_cursor") else None,
                limit=20
            )
            itens, next_cursor = InsumoListCursorDTO.listar_com_cursor(dto)
            results = []
            for insumo in itens:
                results.append({
                    "id_insumo": insumo.id_insumo,
                    "id_movimentacao": insumo.movimentacao_id,
                    "item_insumo": insumo.item_insumo,
                    "created_at": insumo.created_at
                })
            return Response(
                {
                    "results": results,
                    "next_cursor": next_cursor
                },
                status=status.HTTP_200_OK
            )
        except ValueError:
            return Response(
                {"erro": "Parâmetros inválidos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"erro": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
