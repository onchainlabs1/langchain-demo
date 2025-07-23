import pytest
import pandas as pd
import re
from graph.nos import interpretador, executar_analise_dataframe_node


def test_interpretador_analise_tabular():
    pergunta = "Qual é a média da coluna A?"
    resultado = interpretador(pergunta)
    assert resultado == {"proximo_no": "executar_analise_dataframe"}, "Deveria encaminhar para análise de DataFrame."


def test_interpretador_pergunta_geral():
    pergunta = "Qual a capital da França?"
    resultado = interpretador(pergunta)
    assert resultado == {"proximo_no": "encerrar"}, "Deveria encerrar para perguntas não tabulares."


def test_interpretador_palavra_chave_variada():
    pergunta = "Mostre um gráfico da soma dos valores."
    resultado = interpretador(pergunta)
    assert resultado == {"proximo_no": "executar_analise_dataframe"}, "Deveria encaminhar para análise de DataFrame."


def test_interpretador_maiusculas_minusculas():
    pergunta = "QuAl A MÉDIA da COLUNA preço?"
    resultado = interpretador(pergunta)
    assert resultado == {"proximo_no": "executar_analise_dataframe"}, "Deveria ser case-insensitive."


def test_executar_analise_dataframe_node():
    """
    Testa o nó executar_analise_dataframe_node com um DataFrame de exemplo e uma pergunta.
    Verifica se a resposta textual está presente, status é 'ok' e o gráfico (se houver) é válido.
    """
    dados = {
        "Produto": ["A", "B", "C", "D", "E"],
        "Preço": [10.0, 20.0, 30.0, 40.0, 50.0],
        "Quantidade": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(dados)
    entrada = {
        "df": df,
        "pergunta": "Qual é a média da coluna Preço?"
    }
    resultado = executar_analise_dataframe_node(entrada)
    assert resultado["status"] == "ok", f"Status deveria ser 'ok', mas foi: {resultado['status']} ({resultado['mensagem']})"
    assert isinstance(resultado["resposta_textual"], str) and resultado["resposta_textual"].strip() != "", "A resposta textual não pode ser vazia."
    assert re.search(r"\d", resultado["resposta_textual"]), "A resposta deve conter um número."
    if resultado["grafico_base64"] is not None:
        assert isinstance(resultado["grafico_base64"], str), "O gráfico deve ser uma string base64."
        assert resultado["grafico_base64"].startswith("data:image") or resultado["grafico_base64"].startswith("iVBOR"), "O gráfico deve estar em formato base64 de imagem." 