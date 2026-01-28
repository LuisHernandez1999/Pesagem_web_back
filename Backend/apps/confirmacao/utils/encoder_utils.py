import base64
import uuid


def gerar_tag_doc() -> str:
    raw = uuid.uuid4().hex[:10]
    encoded = base64.urlsafe_b64encode(raw.encode()).decode()
    return encoded[:14]
