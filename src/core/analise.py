import base64
import io
import ast
from typing import Tuple, Optional
import pandas as pd

from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_sandbox.executors import PyodideExecutor
from langgraph.graph import StateGraph, END

# Substitua por seu LLM preferido e configuração segura
from langchain_openai import ChatOpenAI

def executar_analise_dataframe(
    df: pd.DataFrame, 
    pergunta: str
) -> Tuple[str, Optional[str]]:
    """
    Executa uma análise segura sobre um DataFrame a partir de uma pergunta em linguagem natural,
    utilizando LangChain, LangGraph e sandbox Pyodide para execução de código Python.

    Parâmetros:
        df (pd.DataFrame): DataFrame com os dados a serem analisados.
        pergunta (str): Pergunta do usuário em português.

    Retorno:
        Tuple[str, Optional[str]]: 
            - Resposta textual em português.
            - Imagem do gráfico em base64 (caso gerado), ou None.
    """
    # 1. Preparar o contexto para o LLM
    contexto = f"""
    Você é um analista de dados. Responda à pergunta do usuário sobre o DataFrame fornecido.
    Gere código Python SEGURO para análise, usando apenas pandas, matplotlib ou altair.
    Nunca acesse rede, arquivos ou comandos do sistema.
    O DataFrame está disponível como 'df'.
    Pergunta: {pergunta}
    """

    # 2. Instanciar o modelo de linguagem (LLM)
    llm: BaseLanguageModel = ChatOpenAI(
        temperature=0.0,
        model="gpt-3.5-turbo",  # ou outro modelo seguro
        streaming=False
    )

    # 3. Gerar o código Python para análise
    prompt = ChatPromptTemplate.from_messages([
        ("system", contexto),
        ("user", "Gere apenas o código Python necessário para responder à pergunta, sem explicações.")
    ])
    codigo_gerado = llm.invoke(prompt).content.strip()

    # 4. Validar o código gerado (proibir comandos perigosos)
    try:
        arvore = ast.parse(codigo_gerado, mode="exec")
        for node in ast.walk(arvore):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Permitir apenas importação de pandas, matplotlib, altair
                nomes = [alias.name for alias in getattr(node, 'names', [])]
                if any(mod not in ("pandas", "matplotlib", "altair", "pyplot") for mod in nomes):
                    raise ValueError("Importação de módulo não permitido.")
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ("open", "exec", "eval", "compile", "os", "sys", "subprocess"):
                    raise ValueError("Uso de função proibida detectado.")
    except Exception as e:
        return (f"Erro de segurança ao validar o código gerado: {e}", None)

    # 5. Executar o código em sandbox seguro (Pyodide)
    executor = PyodideExecutor(
        allowed_imports=["pandas", "matplotlib", "altair"],
        disable_network=True,
        cpu_time_limit=5,
        memory_limit_mb=128
    )
    local_vars = {"df": df}
    resposta_texto = ""
    imagem_base64 = None

    try:
        # Redirecionar saída de gráficos para buffer
        exec_code = (
            "import matplotlib.pyplot as plt\n"
            "import altair as alt\n"
            "import io, base64\n"
            "buffer = io.BytesIO()\n"
            + codigo_gerado +
            "\nif 'plt' in locals() and plt.get_fignums():\n"
            "    plt.savefig(buffer, format='png')\n"
            "    buffer.seek(0)\n"
            "    img_b64 = 'data:image/png;base64,' + base64.b64encode(buffer.read()).decode('utf-8')\n"
            "    resposta = locals().get('resposta', '')\n"
            "else:\n"
            "    img_b64 = None\n"
            "    resposta = locals().get('resposta', '')\n"
        )
        result = executor.execute(exec_code, local_vars=local_vars)
        resposta_texto = result.get("resposta", "").strip() or "Análise concluída."
        imagem_base64 = result.get("img_b64", None)
    except Exception as e:
        resposta_texto = f"Ocorreu um erro ao executar a análise: {e}"
        imagem_base64 = None

    return resposta_texto, imagem_base64 