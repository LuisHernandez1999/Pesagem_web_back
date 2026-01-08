from apps.infra.auth.dto.invite_dto import GenerateInviteDTO
from apps.infra.auth.models.user_invite import UserInvite

class GenerateUserInviteService:
    @staticmethod
    def execute(dto: GenerateInviteDTO) -> UserInvite:
        return UserInvite.create(email=dto.email)
