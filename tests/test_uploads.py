import os
import tempfile
import pytest
from utils.uploads import validar_arquivo_upload, DIRETORIO_UPLOADS


def criar_arquivo_temporario(extensao: str, tamanho_bytes: int) -> str:
    os.makedirs(DIRETORIO_UPLOADS, exist_ok=True)
    fd, caminho = tempfile.mkstemp(suffix=extensao, dir=DIRETORIO_UPLOADS)
    with os.fdopen(fd, "wb") as tmp:
        tmp.write(b"0" * tamanho_bytes)
    return caminho


def test_aceita_csv_ate_10mb():
    caminho = criar_arquivo_temporario(".csv", 10 * 1024 * 1024)
    assert validar_arquivo_upload(caminho) is True
    os.remove(caminho)


def test_aceita_xlsx_ate_10mb():
    caminho = criar_arquivo_temporario(".xlsx", 10 * 1024 * 1024)
    assert validar_arquivo_upload(caminho) is True
    os.remove(caminho)


def test_rejeita_extensao_invalida():
    caminho = criar_arquivo_temporario(".exe", 1024)
    with pytest.raises(ValueError):
        validar_arquivo_upload(caminho)
    os.remove(caminho)


def test_rejeita_arquivo_maior_que_10mb():
    caminho = criar_arquivo_temporario(".csv", 11 * 1024 * 1024)
    with pytest.raises(ValueError):
        validar_arquivo_upload(caminho)
    os.remove(caminho)


def test_rejeita_arquivo_fora_do_uploads():
    fd, caminho = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "wb") as tmp:
        tmp.write(b"0" * 1024)
    with pytest.raises(ValueError):
        validar_arquivo_upload(caminho)
    os.remove(caminho) 