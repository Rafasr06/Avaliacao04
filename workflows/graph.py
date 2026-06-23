print("GRAPH V1 CARREGADO")
from typing import TypedDict, List, Optional
from langgraph.checkpoint.postgres import PostgresSaver

from langgraph.graph import StateGraph, END


from agents.orchestrator import decidir_agente

from agents.secretary_agent import executar_secretario
from agents.python_agent import executar_python_agent
from agents.banco_agent import executar_banco_agent
from agents.algoritmos_agent import executar_algoritmos_agent
from agents.engenharia_agent import executar_engenharia_agent


from memory.memory_manager import memory_manager

from tools.conversa_tools import salvar_mensagem
from tools.topico_tools import contar_topicos_concluidos



# ==============================
# Estado do Workflow
# ==============================

class WorkflowState(TypedDict):

    student_id: int

    materia_id: int

    message: str

    current_subject: Optional[str]

    completed_topics: List

    current_topic: Optional[str]

    conversation_history: List

    last_agent: Optional[str]

    response: str

    next_agent: str



# ==============================
# Nó Entrada
# ==============================

def entrada(state: WorkflowState):

    mensagem = state["message"]

    aluno = state["student_id"]


    memory_manager.adicionar_mensagem_global(
        aluno,
        mensagem
    )


    state["conversation_history"].append(
        {
            "role": "user",
            "content": mensagem
        }
    )


    return state



# ==============================
# Orquestrador
# ==============================

def orquestrador(state: WorkflowState):

    print("ESTADO RECEBIDO NO ORQUESTRADOR:")
    print(state)

    materia_atual = state.get("current_subject")

    agente_desejado = decidir_agente(
        state["message"]
    )

    if agente_desejado == "desconhecido":

        if state.get("current_subject"):

            agente_desejado = state["current_subject"]

        else:

            agente_desejado = "secretario"

    if (
    materia_atual
    and agente_desejado != "desconhecido"
    and agente_desejado != materia_atual
):

            print("TENTATIVA DE TROCA DE MATÉRIA")
    print("Atual:", materia_atual)
    print("Nova:", agente_desejado)

    total_concluidos = contar_topicos_concluidos.invoke(
        {
            "aluno_id": state["student_id"]
        }
    )

    print("TOTAL CONCLUÍDOS:", total_concluidos)

    if total_concluidos == 0:

        state["response"] = (
            "Você precisa concluir pelo menos "
            "um tópico antes de trocar de matéria."
        )

        state["last_agent"] = "orchestrator"
        state["next_agent"] = "secretario"

        return state
    state["next_agent"] = agente_desejado

    state["last_agent"] = "orchestrator"

    print(
        "PRÓXIMO AGENTE:",
        agente_desejado
    )

    return state



# ==============================
# Agentes
# ==============================


def secretario_node(state: WorkflowState):


    resposta = executar_secretario(
        state["message"]
    )


    state["response"] = resposta

    state["last_agent"] = "secretario"


    return state



def python_node(state: WorkflowState):


    resposta = executar_python_agent(
        state["message"]
    )


    state["response"] = resposta


    state["last_agent"] = "python"


    state["materia_id"] = 2


    state["current_subject"] = "python"


    return state



def banco_node(state):

    print("ENTROU NO BANCO NODE")

    resposta = executar_banco_agent(
        state["message"]
    )

    state["response"] = resposta

    state["last_agent"] = "banco"

    state["materia_id"] = 1

    state["current_subject"] = "banco"

    print("CURRENT SUBJECT:", state["current_subject"])

    return state



def algoritmos_node(state: WorkflowState):


    resposta = executar_algoritmos_agent(
        state["message"]
    )


    state["response"] = resposta


    state["last_agent"] = "algoritmos"


    state["materia_id"] = 3


    state["current_subject"] = "algoritmos"


    return state



def engenharia_node(state: WorkflowState):


    resposta = executar_engenharia_agent(
        state["message"]
    )


    state["response"] = resposta


    state["last_agent"] = "engenharia"


    state["materia_id"] = 4


    state["current_subject"] = "engenharia"


    return state




# ==============================
# Escolha próximo nó
# ==============================


def escolher_proximo_no(state):

    return state["next_agent"]




# ==============================
# Persistência
# ==============================


def persistencia(state: WorkflowState):


    aluno = state["student_id"]



    memory_manager.adicionar_mensagem_global(
        aluno,
        state["response"]
    )



    state["conversation_history"].append(
        {
            "role": "assistant",
            "content": state["response"]
        }
    )



    salvar_mensagem.invoke(
        {
            "aluno_id": aluno,
            "materia_id": state.get(
                "materia_id",
                1
            ),
            "role": "assistant",
            "conteudo": state["response"]
        }
    )



    return state




def salvar_usuario(state: WorkflowState):


    salvar_mensagem.invoke(
        {
            "aluno_id": state["student_id"],

            "materia_id": state.get(
                "materia_id",
                1
            ),

            "role": "user",

            "conteudo": state["message"]
        }
    )


    return state




# ==============================
# Finalização
# ==============================


def finalizacao(state):

    return state




# ==============================
# Construção do Grafo
# ==============================


workflow = StateGraph(
    WorkflowState
)



workflow.add_node(
    "entrada",
    entrada
)


workflow.add_node(
    "salvar_usuario",
    salvar_usuario
)



workflow.add_node(
    "orquestrador",
    orquestrador
)



workflow.add_node(
    "secretario",
    secretario_node
)



workflow.add_node(
    "python",
    python_node
)



workflow.add_node(
    "banco",
    banco_node
)



workflow.add_node(
    "algoritmos",
    algoritmos_node
)



workflow.add_node(
    "engenharia",
    engenharia_node
)



workflow.add_node(
    "persistencia",
    persistencia
)



workflow.add_node(
    "finalizacao",
    finalizacao
)




# ==============================
# Fluxo
# ==============================


workflow.set_entry_point(
    "entrada"
)



workflow.add_edge(
    "entrada",
    "salvar_usuario"
)



workflow.add_edge(
    "salvar_usuario",
    "orquestrador"
)



workflow.add_conditional_edges(
    "orquestrador",
    escolher_proximo_no,
    {

        "secretario": "secretario",

        "python": "python",

        "banco": "banco",

        "algoritmos": "algoritmos",

        "engenharia": "engenharia"

    }
)



workflow.add_edge(
    "secretario",
    "persistencia"
)



workflow.add_edge(
    "python",
    "persistencia"
)



workflow.add_edge(
    "banco",
    "persistencia"
)



workflow.add_edge(
    "algoritmos",
    "persistencia"
)



workflow.add_edge(
    "engenharia",
    "persistencia"
)



workflow.add_edge(
    "persistencia",
    "finalizacao"
)



workflow.add_edge(
    "finalizacao",
    END
)



# ==============================
# Compilar
# ==============================


app = workflow.compile()
