from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from apps.infra.auth.adapters.invite import generate_invite_adapter
from apps.infra.auth.service.generate_invite import GenerateUserInviteService

class GenerateInviteAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        dto = generate_invite_adapter(request)
        invite = GenerateUserInviteService.execute(dto)

        return Response(
            {
                "invite_link": f"https://frontend/register?token={invite.token}"
            },
            status=status.HTTP_201_CREATED,
        )
