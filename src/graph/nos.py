from typing import Dict, Any
import pandas as pd
from core.analise import executar_analise_dataframe


def interpretador(pergunta: str) -> Dict[str, str]:
    """
    Nó interpretador do fluxo LangGraph.
    Decide se a pergunta do usuário deve ser encaminhada para análise de DataFrame
    ou se o fluxo deve ser encerrado.

    Parâmetros:
        pergunta (str): Pergunta do usuário em português.

    Retorno:
        dict: Dicionário com a chave 'proximo_no', indicando o próximo nó do fluxo.
              Pode ser 'executar_analise_dataframe' ou 'encerrar'.
    """
    # Palavras-chave que indicam análise tabular
    palavras_chave = [
        "coluna", "média", "media", "gráfico", "grafico", "dataframe", "tabela",
        "linha", "soma", "contagem", "quantidade", "valor", "máximo", "minimo", "mínimo", "máximo"
    ]
    pergunta_lower = pergunta.lower()
    if any(palavra in pergunta_lower for palavra in palavras_chave):
        return {"proximo_no": "executar_analise_dataframe"}
    else:
        return {"proximo_no": "encerrar"}


def executar_analise_dataframe_node(entrada: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nó do LangGraph responsável por executar a análise do DataFrame.
    Recebe um dicionário com o DataFrame e a pergunta, chama a função de análise
    e retorna a resposta, gráfico (se houver), status e mensagem para logs.

    Parâmetros:
        entrada (dict): Deve conter as chaves 'df' (DataFrame) e 'pergunta' (str).

    Retorno:
        dict: Contém 'resposta_textual', 'grafico_base64', 'status' e 'mensagem'.
    """
    try:
        df = entrada["df"]
        pergunta = entrada["pergunta"]
        resposta, grafico = executar_analise_dataframe(df, pergunta)
        return {
            "resposta_textual": resposta,
            "grafico_base64": grafico,
            "status": "ok",
            "mensagem": "Análise realizada com sucesso."
        }
    except Exception as e:
        return {
            "resposta_textual": "",
            "grafico_base64": None,
            "status": "erro",
            "mensagem": f"Erro ao executar análise: {e}"
        } 