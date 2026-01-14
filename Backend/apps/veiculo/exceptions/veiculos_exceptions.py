
class VeiculoException(Exception):
    status_code = 400
    default_detail = "Erro relacionado ao veículo"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class VeiculoAlreadyExists(VeiculoException):
    status_code = 409
    default_detail = "Veículo já cadastrado"


class PrefixoAlreadyExists(VeiculoAlreadyExists):
    default_detail = "Prefixo já cadastrado"


class PlacaAlreadyExists(VeiculoAlreadyExists):
    default_detail = "Placa já cadastrada"


class InvalidCursorException(VeiculoException):
    status_code = 400
    default_detail = "Cursor inválido"


class InvalidPayloadException(VeiculoException):
    status_code = 422
    default_detail = "Payload inválido"
