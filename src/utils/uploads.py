import os
from typing import Any

TAMANHO_MAXIMO_MB = 10
EXTENSOES_PERMITIDAS = {".csv", ".xlsx"}
DIRETORIO_UPLOADS = os.path.abspath("uploads")


def validar_arquivo_upload(caminho_arquivo: str, diretorio_base: str = DIRETORIO_UPLOADS) -> bool:
    """
    Valida se o arquivo enviado atende aos requisitos de segurança:
    - Extensão permitida (.csv, .xlsx)
    - Tamanho até 10 MB
    - Caminho deve estar dentro do diretório de uploads
    """
    _, extensao = os.path.splitext(caminho_arquivo)
    if extensao.lower() not in EXTENSOES_PERMITIDAS:
        raise ValueError("Extensão de arquivo não permitida. Apenas CSV ou XLSX.")
    if os.path.getsize(caminho_arquivo) > TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise ValueError("Arquivo excede o tamanho máximo de 10 MB.")
    caminho_absoluto = os.path.abspath(caminho_arquivo)
    if not caminho_absoluto.startswith(diretorio_base):
        raise ValueError("Arquivo fora do diretório de uploads permitido.")
    return True 