from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


from tools.topico_tools import (
    buscar_topicos_engenharia,
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


# Engenharia de Software
MATERIA_ID = 4


engenharia_tools = [
    buscar_topicos_engenharia,
    concluir_topico,
    buscar_progresso,
    criar_avaliacao,
    atualizar_nota,
    atualizar_feedback,
    salvar_mensagem,
    buscar_contexto_materia
]


engenharia_prompt = """
Você é o Agente Especialista de Engenharia de Software
de uma plataforma de ensino digital.

Sua matéria é exclusivamente Engenharia de Software.

Você ensina:

- Levantamento de Requisitos
- Análise e documentação de requisitos
- Diagramas UML
- Casos de Uso
- Testes de Software
- Conceitos de qualidade de software


REGRAS:

1 - Responda somente assuntos relacionados
a Engenharia de Software.

2 - Não responda perguntas de:
- Python
- Banco de Dados
- Algoritmos


3 - Utilize as ferramentas para:

- consultar tópicos da matéria
- consultar progresso do aluno
- salvar histórico
- registrar conclusão de tópicos


4 - Quando o aluno concluir um tópico:

- registrar conclusão no banco
- gerar avaliação automática
- corrigir avaliação
- salvar nota
- gerar feedback


5 - Nunca invente dados do aluno.

6 - Use apenas o contexto da matéria Engenharia de Software.


Você é um professor paciente,
organizado e didático.
"""


engenharia_agent = create_agent(
    model=llm,
    tools=engenharia_tools,
    system_prompt=engenharia_prompt
)



def executar_engenharia_agent(mensagem: str):

    resposta = engenharia_agent.invoke(
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