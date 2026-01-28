class CelularException(Exception):
    pass


class CelularNumeroDuplicado(CelularException):
    def __init__(self):
        super().__init__("Já existe um celular com esse número")


class CelularApelidoDuplicado(CelularException):
    def __init__(self):
        super().__init__("Já existe um celular com esse apelido")


class CelularImeiDuplicado(CelularException):
    def __init__(self):
        super().__init__("Já existe um celular com esse IMEI")


class CelularCampoObrigatorio(CelularException):
    def __init__(self, campo: str):
        super().__init__(f"O campo '{campo}' é obrigatório")
