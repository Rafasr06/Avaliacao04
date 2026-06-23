from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


from agents.secretary_agent import executar_secretario
from agents.python_agent import executar_python_agent
from agents.banco_agent import executar_banco_agent
from agents.algoritmos_agent import executar_algoritmos_agent
from agents.engenharia_agent import executar_engenharia_agent



llm = ChatOpenAI(
    model="gpt-5.4-mini",
    temperature=0
)



orchestrator_prompt = """
Você é o agente Orquestrador de uma plataforma
de ensino digital.

Sua função NÃO é responder perguntas.
Sua função é decidir qual agente especialista
deve atender o aluno.


REGRAS DE ROTEAMENTO:


1 - Perguntas administrativas:

Exemplos:

- matrícula
- cadastro
- matérias disponíveis
- progresso geral
- remover matrícula

Enviar para:

SECRETÁRIO


2 - Perguntas sobre Python:

Enviar para:

PYTHON_AGENT


3 - Perguntas sobre Banco de Dados:

Enviar para:

BANCO_AGENT


4 - Perguntas sobre Algoritmos:

Enviar para:

ALGORITMOS_AGENT


5 - Perguntas sobre Engenharia de Software:

Enviar para:

ENGENHARIA_AGENT


Nunca ensine conteúdo.
Somente encaminhe.
"""
def decidir_agente(mensagem):

    mensagem_lower = mensagem.lower()

    if any(
        palavra in mensagem_lower
        for palavra in [
            "matricula",
            "matrícula",
            "matricular",
            "cadastro",
            "progresso",
            "remover"
        ]
    ):
        return "secretario"

    elif any(
        palavra in mensagem_lower
        for palavra in [
            "python",
            "função",
            "classe",
            "variavel"
        ]
    ):
        return "python"

    elif any(
    palavra in mensagem_lower
    for palavra in [
        "sql",
        "banco",
        "select",
        "normalização",
        "tabela",
        "join",
        "inner join",
        "left join",
        "concluir topico"
    ]
):
     return "banco"

    elif any(
        palavra in mensagem_lower
        for palavra in [
            "algoritmo",
            "if",
            "else",
            "for",
            "while"
        ]
    ):
        return "algoritmos"

    elif any(
        palavra in mensagem_lower
        for palavra in [
            "uml",
            "requisito",
            "teste de software",
            "caso de uso"
        ]
    ):
        return "engenharia"

    return "desconhecido"



def executar_orquestrador(mensagem):

    mensagem_lower = mensagem.lower()


    if any(
        palavra in mensagem_lower
        for palavra in [
            "matrícula",
            "matrícular",
            "cadastro",
            "progresso",
            "remover"
        ]
    ):
        return executar_secretario(mensagem)



    elif any(
        palavra in mensagem_lower
        for palavra in [
            "python",
            "função",
            "classe",
            "variavel"
        ]
    ):
        return executar_python_agent(mensagem)



    elif any(
        palavra in mensagem_lower
        for palavra in [
            "sql",
            "banco",
            "select",
            "normalização",
            "tabela"
        ]
    ):
        return executar_banco_agent(mensagem)



    elif any(
        palavra in mensagem_lower
        for palavra in [
            "algoritmo",
            "if",
            "else",
            "for",
            "while"
        ]
    ):
        return executar_algoritmos_agent(mensagem)



    elif any(
        palavra in mensagem_lower
        for palavra in [
            "uml",
            "requisito",
            "teste de software",
            "caso de uso"
        ]
    ):
        return executar_engenharia_agent(mensagem)



    else:
        return (
            "Não consegui identificar a matéria. "
            "Informe se sua dúvida é sobre Python, "
            "Banco de Dados, Algoritmos ou Engenharia de Software."
        )