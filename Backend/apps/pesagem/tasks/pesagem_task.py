# pesagem/tasks.py
from celery import shared_task
from  apps.pesagem.service.pesagem_service import PesagemServiceDoc,  PesagemCreateDocDTO
from apps.pesagem.documents.doc_generator import PesagemExcelDocument
import io
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

@shared_task
def gerar_relatorio_pesagem_task(dto_dict):
    dto = PesagemCreateDocDTO(**dto_dict)
    dados = PesagemServiceDoc.executar(dto)
    wb = PesagemExcelDocument.gerar(dados)
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    file_name = f"relatorios/relatorio_pesagens_{dto.start_date}_{dto.end_date}.xlsx"
    default_storage.save(file_name, ContentFile(buffer.read()))

    return file_name  
