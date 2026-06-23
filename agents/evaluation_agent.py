from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.conversa_tools import buscar_contexto_materia, salvar_mensagem
from tools.avaliacao_tools import criar_avaliacao, atualizar_nota, atualizar_feedback
import json


llm_avaliador = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

llm_corretor = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1
)


def gerar_3_questoes(materia_id: int, topico: str, aluno_id: int):
    """Gera 3 questões diferentes sobre um tópico usando IA."""

    # Carregar contexto das conversas anteriores
    contexto = buscar_contexto_materia.invoke(
        {"materia_id": materia_id}
    )

    historico_txt = "\n".join(
        [f"{role}: {conteudo}" for role, conteudo in contexto]
    )

    prompt_gerador = f"""
    Você é um professor gerando 3 exercícios/questões diferentes sobre o tópico: {topico}
    
    Histórico da conversa com o aluno:
    {historico_txt}
    
    Gere 3 questões variadas (múltipla escolha, verdadeiro/falso, discursiva).
    Cada questão deve testar diferentes aspectos do tópico.
    
    Responda em JSON com este formato:
    {{
        "questoes": [
            {{
                "numero": 1,
                "tipo": "multipla_escolha",
                "enunciado": "...",
                "opcoes": ["a) ...", "b) ...", "c) ...", "d) ..."],
                "resposta_correta": "a"
            }},
            ...
        ]
    }}
    """

    resposta = llm_avaliador.invoke(
        [{"role": "user", "content": prompt_gerador}]
    )

    try:
        questoes_data = json.loads(resposta.content)
        return questoes_data["questoes"]
    except:
        # Fallback se não conseguir parsear JSON
        return [
            {
                "numero": 1,
                "tipo": "discursiva",
                "enunciado": f"Explique os conceitos principais de {topico}.",
                "resposta_correta": "Resposta em aberto"
            },
            {
                "numero": 2,
                "tipo": "discursiva",
                "enunciado": f"Cite um exemplo prático de {topico}.",
                "resposta_correta": "Resposta em aberto"
            },
            {
                "numero": 3,
                "tipo": "discursiva",
                "enunciado": f"Qual é a importância de {topico}?",
                "resposta_correta": "Resposta em aberto"
            }
        ]


def corrigir_respostas(questoes: list, respostas: list, topico: str):
    """Corrige automaticamente as respostas do aluno."""

    questoes_str = json.dumps(questoes, ensure_ascii=False, indent=2)
    respostas_str = json.dumps(respostas, ensure_ascii=False, indent=2)

    prompt_corretor = f"""
    Você é um professor corrigindo avaliações sobre: {topico}
    
    QUESTÕES:
    {questoes_str}
    
    RESPOSTAS DO ALUNO:
    {respostas_str}
    
    Para cada resposta, analise e gere:
    1. Uma nota de 0 a 10
    2. Um feedback construtivo
    
    Responda em JSON:
    {{
        "correcoes": [
            {{
                "numero_questao": 1,
                "nota": 8,
                "feedback": "Muito bom, apenas faltou..."
            }},
            ...
        ]
    }}
    """

    resposta = llm_corretor.invoke(
        [{"role": "user", "content": prompt_corretor}]
    )

    try:
        correcoes_data = json.loads(resposta.content)
        return correcoes_data["correcoes"]
    except:
        return [
            {"numero_questao": i+1, "nota": 7, "feedback": "Bom desempenho geral."}
            for i in range(len(respostas))
        ]


def criar_3_avaliacoes_com_questoes(
    aluno_id: int,
    materia_id: int,
    topico_id: int,
    titulo_topico: str
):
    """
    Cria 3 avaliações com questões diferentes e retorna os IDs.
    """

    questoes = gerar_3_questoes(materia_id, titulo_topico, aluno_id)

    avaliacao_ids = []

    for i, questao in enumerate(questoes):
        titulo = f"Avaliação {i+1} - {titulo_topico}"

        avaliacao_id = criar_avaliacao.invoke(
            {
                "aluno_id": aluno_id,
                "materia_id": materia_id,
                "titulo": titulo
            }
        )

        # Salvar questão como conteúdo da avaliação
        questao_json = json.dumps(questao, ensure_ascii=False)

        salvar_mensagem.invoke(
            {
                "materia_id": materia_id,
                "role": "system",
                "conteudo": f"QUESTÃO {avaliacao_id}: {questao_json}"
            }
        )

        avaliacao_ids.append(avaliacao_id)

    return {
        "questoes": questoes,
        "avaliacao_ids": avaliacao_ids
    }


def corrigir_3_avaliacoes(
    aluno_id: int,
    materia_id: int,
    avaliacao_ids: list,
    respostas_aluno: list,
    topico: str
):
    """
    Corrige as 3 avaliações e armazena notas e feedbacks.
    """

    # Buscar questões
    contexto = buscar_contexto_materia.invoke(
        {"materia_id": materia_id}
    )

    questoes_recuperadas = []
    for role, conteudo in contexto:
        if "QUESTÃO" in conteudo:
            try:
                questao_json = conteudo.split("QUESTÃO")[1].split(":")[1].strip()
                questoes_recuperadas.append(json.loads(questao_json))
            except:
                pass

    # Corrigir respostas
    correcoes = corrigir_respostas(questoes_recuperadas, respostas_aluno, topico)

    resultados = []

    for i, (avaliacao_id, correcao) in enumerate(
        zip(avaliacao_ids, correcoes)
    ):
        nota = correcao.get("nota", 5)
        feedback = correcao.get("feedback", "")

        atualizar_nota.invoke(
            {"avaliacao_id": avaliacao_id, "nota": nota}
        )

        atualizar_feedback.invoke(
            {"avaliacao_id": avaliacao_id, "feedback": feedback}
        )

        resultados.append(
            {
                "avaliacao_id": avaliacao_id,
                "nota": nota,
                "feedback": feedback
            }
        )

        salvar_mensagem.invoke(
            {
                "materia_id": materia_id,
                "role": "assistant",
                "conteudo": f"Avaliação {i+1} corrigida: {nota}/10 - {feedback}"
            }
        )

    return resultados
