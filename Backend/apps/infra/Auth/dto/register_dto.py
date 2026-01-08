from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserDTO:
    email: str
    password: str



@dataclass
class RegisterByInviteDTO:
    token: str
    email: str
    password: str