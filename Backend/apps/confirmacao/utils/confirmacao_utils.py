from apps.confirmacao.exceptions.exceptions_confirmacao import DadosInvalidosError



import uuid
from django.conf import settings
from config.r2_client import get_r2_client


def upload_imagem_confirmacao(file) -> str:
    client = get_r2_client()

    extensao = file.name.split(".")[-1]
    key = f"confirmacoes/{uuid.uuid4()}.{extensao}"

    client.upload_fileobj(
        Fileobj=file,
        Bucket=settings.R2_BUCKET_NAME,
        Key=key,
        ExtraArgs={
            "ContentType": file.content_type,
        },
    )

    return f"{settings.R2_PUBLIC_BASE_URL}/{key}"

def validar_confirmacao(dto):
    if not dto.data_servico:
        raise DadosInvalidosError("data_servico é obrigatória")

    if not dto.tipo_servico:
        raise DadosInvalidosError("tipo_servico é obrigatório")

    if not dto.imagens:
        raise DadosInvalidosError("É necessário ao menos uma imagem")
