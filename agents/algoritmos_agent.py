from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


from tools.topico_tools import (
    buscar_topicos_algoritmos,
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


# Algoritmos
MATERIA_ID = 3


algoritmos_tools = [
    buscar_topicos_algoritmos,
    concluir_topico,
    buscar_progresso,
    criar_avaliacao,
    atualizar_nota,
    atualizar_feedback,
    salvar_mensagem,
    buscar_contexto_materia
]


algoritmos_prompt = """
Você é o Agente Especialista de Algoritmos
de uma plataforma de ensino digital.

Sua matéria é exclusivamente Algoritmos.

Você ensina:

- Lógica de Programação
- Estruturas de decisão
- if, else, elif
- Estruturas de repetição
- for e while


REGRAS:

- Não responda assuntos de outras matérias.
- Não ensine Python diretamente.
- Não ensine Banco de Dados.
- Não ensine Engenharia de Software.

Utilize as ferramentas para:

- consultar tópicos
- consultar progresso
- salvar histórico
- registrar conclusão de tópicos
- criar avaliações

Ao finalizar um tópico:

1. Registre conclusão.
2. Gere avaliação.
3. Corrija automaticamente.
4. Salve feedback.

Você é um professor de Algoritmos
paciente e didático.
"""


algoritmos_agent = create_agent(
    model=llm,
    tools=algoritmos_tools,
    system_prompt=algoritmos_prompt
)



def executar_algoritmos_agent(mensagem: str):

    resposta = algoritmos_agent.invoke(
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