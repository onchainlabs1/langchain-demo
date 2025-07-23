import pytest
import pandas as pd
import re
from core.analise import executar_analise_dataframe


def test_executar_analise_dataframe():
    """
    Testa a função executar_analise_dataframe com um DataFrame simples e uma pergunta sobre a média dos preços.
    Verifica se a resposta está em português, contém um número e se o gráfico (se houver) está em base64.
    """
    # 1. Criar DataFrame de exemplo
    dados = {
        "Produto": ["A", "B", "C", "D", "E"],
        "Preço": [10.0, 20.0, 30.0, 40.0, 50.0],
        "Quantidade": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(dados)

    # 2. Pergunta em português
    pergunta = "Qual é a média da coluna Preço?"

    # 3. Chamar a função de análise
    try:
        resposta, grafico_base64 = executar_analise_dataframe(df, pergunta)
    except Exception as e:
        pytest.fail(f"Erro ao executar a análise: {e}")

    # 4. Verificações
    assert isinstance(resposta, str), "A resposta deve ser uma string."
    assert resposta.strip() != "", "A resposta não pode ser vazia."
    assert re.search(r"\d", resposta), "A resposta deve conter um número."
    assert any(palavra in resposta.lower() for palavra in ["média", "preço"]), "A resposta deve estar em português e mencionar 'média' ou 'preço'."

    if grafico_base64 is not None:
        assert isinstance(grafico_base64, str), "O gráfico deve ser uma string base64."
        assert grafico_base64.startswith("data:image") or grafico_base64.startswith("iVBOR"), "O gráfico deve estar em formato base64 de imagem."

    # 5. Mensagem de sucesso
    print("Teste de análise de DataFrame executado com sucesso.") 