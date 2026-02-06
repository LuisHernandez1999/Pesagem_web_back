from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from celery.result import AsyncResult


class ReportStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, task_id):
        result = AsyncResult(task_id)

        response = {
            "task_id": task_id,
            "status": result.status,
        }

        if result.status == "SUCCESS":
            response["arquivo"] = result.result.get("arquivo")

        return Response(response)