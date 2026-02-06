import os
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ReportDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, nome_arquivo):
        base_path = "/caminho/relatorios"
        caminho = os.path.join(base_path, nome_arquivo)

        if not os.path.exists(caminho):
            return Response(
                {"erro": "Arquivo não encontrado"},
                status=404,
            )

        return FileResponse(
            open(caminho, "rb"),
            as_attachment=True,
            filename=nome_arquivo,
        )