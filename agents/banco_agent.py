from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


from tools.topico_tools import (
    buscar_topicos,
    concluir_topico,
    buscar_progresso,
    finalizar_topico
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


# Banco de Dados
MATERIA_ID = 1


banco_tools = [
    buscar_topicos,
    concluir_topico,
    buscar_progresso,
    criar_avaliacao,
    atualizar_nota,
    atualizar_feedback,
    salvar_mensagem,
    buscar_contexto_materia
]


banco_prompt = """
Você é o Agente Especialista de Banco de Dados
de uma plataforma de ensino digital.

Sua matéria é exclusivamente Banco de Dados.

Você ensina:

- Modelo Relacional
- SQL Básico
- SELECT, INSERT, UPDATE e DELETE
- Normalização
- Organização e modelagem de dados


REGRAS:

1 - Responda somente assuntos relacionados
a Banco de Dados.

2 - Não ensine Python,
Algoritmos ou Engenharia de Software.

3 - Utilize as ferramentas disponíveis para:

- consultar tópicos da matéria
- consultar progresso do aluno
- salvar histórico da conversa
- registrar conclusão de tópicos


4 - Quando o aluno dominar um tópico:

- registre a conclusão
- gere uma avaliação automática
- corrija a avaliação
- gere feedback
- salve os dados


5 - Nunca invente dados do aluno.
Sempre consulte o banco quando necessário.


Você é um professor de Banco de Dados,
paciente e didático.
"""


banco_agent = create_agent(
    model=llm,
    tools=banco_tools,
    system_prompt=banco_prompt
)


def executar_banco_agent(mensagem: str):

    if "concluir topico" in mensagem.lower():

        return finalizar_topico(
            aluno_id=1,
            materia_id=1,
            topico_id=1,
            titulo_topico="JOIN"
        )

    contexto = buscar_contexto_materia.invoke(
        {
            "materia_id": 1
        }
    )

    mensagens = []

    for role, conteudo in reversed(contexto):

        mensagens.append(
            {
                "role": role,
                "content": conteudo
            }
        )

    mensagens.append(
        {
            "role": "user",
            "content": mensagem
        }
    )

    resposta = banco_agent.invoke(
        {
            "messages": mensagens
        }
    )

    return resposta["messages"][-1].content