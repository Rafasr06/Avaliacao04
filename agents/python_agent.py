from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


from tools.topico_tools import (
    buscar_topicos,
    concluir_topico,
    buscar_progresso
)

from tools.avaliacao_tools import (
    criar_avaliacao,
    atualizar_nota,
    atualizar_feedback
)

from tools.conversa_tools import (
    salvar_mensagem,
    buscar_contexto_materia
)


llm = ChatOpenAI(
    model="gpt-5.4-mini",
    temperature=0.3
)


# Matéria fixa do agente
MATERIA_ID = 2


python_tools = [
    buscar_topicos,
    concluir_topico,
    buscar_progresso,
    criar_avaliacao,
    atualizar_nota,
    atualizar_feedback,
    salvar_mensagem,
    buscar_contexto_materia
]


python_prompt = """
Você é o Agente Especialista de Python
de uma plataforma de ensino digital.

Sua matéria é exclusivamente Python.

Você deve ensinar:

- Variáveis e tipos de dados
- Funções
- Programação Orientada a Objetos
- Lógica de programação em Python


REGRAS:

1 - Você só pode responder assuntos relacionados a Python.

2 - Não responda perguntas de outras matérias.

3 - Utilize as ferramentas para:
- consultar tópicos
- verificar progresso do aluno
- salvar histórico
- registrar conclusão de tópicos


4 - Quando o aluno demonstrar domínio de um tópico:

- registre a conclusão
- gere uma avaliação automática
- corrija a avaliação
- gere feedback
- salve o resultado


5 - Nunca invente informações do banco.

6 - Utilize apenas o contexto da matéria Python.

Você é um professor paciente,
didático e orientado ao aprendizado.
"""


python_agent = create_agent(
    model=llm,
    tools=python_tools,
    system_prompt=python_prompt
)



def executar_python_agent(mensagem: str):

    resposta = python_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": mensagem
                }
            ]
        }
    )

    return resposta["messages"][-1].content