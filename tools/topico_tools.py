from langchain_core.tools import tool
from database.connection import get_connection

from tools.avaliacao_tools import (
    criar_avaliacao,
    atualizar_nota,
    atualizar_feedback
)


@tool
def buscar_topicos(materia_id: int):
    """Busca tópicos de uma matéria."""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, titulo, descricao, ordem
        FROM topico
        WHERE materia_id = %s
        ORDER BY ordem
        """,
        (materia_id,)
    )

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@tool
def concluir_topico(aluno_id: int, topico_id: int):
    """Marca tópico como concluído."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO topico_aluno (aluno_id, topico_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        (aluno_id, topico_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return "Tópico concluído"


@tool
def buscar_progresso(aluno_id: int):
    """Retorna progresso do aluno."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            materia.nome,
            COUNT(topico.id) AS total_topicos,
            COUNT(topico_aluno.id) AS concluidos
        FROM matricula
        JOIN materia
            ON materia.id = matricula.materia_id
        JOIN topico
            ON topico.materia_id = materia.id
        LEFT JOIN topico_aluno
            ON topico_aluno.topico_id = topico.id
            AND topico_aluno.aluno_id = %s
        WHERE matricula.aluno_id = %s
        GROUP BY materia.nome
        """,
        (aluno_id, aluno_id)
    )

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@tool
def buscar_topicos_algoritmos():
    """Busca tópicos da matéria Algoritmos."""

    return buscar_topicos.invoke(
        {
            "materia_id": 3
        }
    )


@tool
def buscar_topicos_engenharia():
    """Busca tópicos da matéria Engenharia de Software."""

    return buscar_topicos.invoke(
        {
            "materia_id": 4
        }
    )


def finalizar_topico(
    aluno_id,
    materia_id,
    topico_id,
    titulo_topico
):

    concluir_topico.invoke(
        {
            "aluno_id": aluno_id,
            "topico_id": topico_id
        }
    )

    avaliacao_id = criar_avaliacao.invoke(
        {
            "aluno_id": aluno_id,
            "materia_id": materia_id,
            "titulo": f"Avaliação - {titulo_topico}"
        }
    )

    atualizar_nota.invoke(
        {
            "avaliacao_id": avaliacao_id,
            "nota": 10
        }
    )

    atualizar_feedback.invoke(
        {
            "avaliacao_id": avaliacao_id,
            "feedback": "Aluno demonstrou domínio do tópico."
        }
    )

    return (
        f"Tópico '{titulo_topico}' concluído. "
        f"Avaliação criada com nota 10."
    )
@tool
def contar_topicos_concluidos(aluno_id: int):
    """Conta quantos tópicos o aluno concluiu."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM topico_aluno
        WHERE aluno_id = %s
        """,
        (aluno_id,)
    )

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total
@tool
def verificar_topico_concluido(aluno_id: int, topico_id: int):
    """
    Verifica se o aluno já concluiu o tópico.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM topico_aluno
        WHERE aluno_id = %s
        AND topico_id = %s
        """,
        (
            aluno_id,
            topico_id
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado is not None