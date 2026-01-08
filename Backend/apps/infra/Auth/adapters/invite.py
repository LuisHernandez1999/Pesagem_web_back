from apps.infra.auth.dto.invite_dto import GenerateInviteDTO

def generate_invite_adapter(request) -> GenerateInviteDTO:
    return GenerateInviteDTO(
        email=request.data["email"]
    )
