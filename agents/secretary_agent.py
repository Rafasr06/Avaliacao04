from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools.aluno_tools import buscar_aluno, criar_aluno
from tools.matricula_tools import (
    matricular_aluno,
    remover_matricula,
    listar_materias_aluno
)

from tools.topico_tools import buscar_progresso


# Modelo da OpenAI
llm = ChatOpenAI(
    model="gpt-5.4-mini",
    temperature=0
)


# Tools permitidas pelo secretário
secretary_tools = [
    buscar_aluno,
    criar_aluno,
    buscar_progresso
]


# Prompt do agente
secretary_prompt = """
Você é o Agente Secretário de uma plataforma de ensino digital.

Sua função é exclusivamente administrativa.

Você pode:
- consultar alunos
- cadastrar alunos quando solicitado
- realizar matrículas
- remover matrículas
- listar matérias disponíveis ao aluno
- consultar progresso geral

REGRAS IMPORTANTES:

- Você NÃO ensina conteúdos.
- Você NÃO responde dúvidas de matérias.
- Você NÃO corrige avaliações.
- Quando o aluno perguntar algo pedagógico,
  informe que deve falar com o agente especialista da matéria.

Sempre utilize as ferramentas disponíveis
para buscar ou alterar informações no banco.
"""


# Criando agente
secretary_agent = create_agent(
    model=llm,
    tools=secretary_tools,
    system_prompt=secretary_prompt
)


def executar_secretario(mensagem: str):

    resposta = secretary_agent.invoke(
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

