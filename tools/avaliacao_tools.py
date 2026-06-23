from langchain_core.tools import tool
from database.connection import get_connection


@tool
def criar_avaliacao(aluno_id: int, materia_id: int, titulo: str):
    """Cria avaliação."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO avaliacao (aluno_id, materia_id, titulo)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (aluno_id, materia_id, titulo)
    )

    avaliacao_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return avaliacao_id


@tool
def atualizar_nota(avaliacao_id: int, nota: float):
    """Atualiza nota da avaliação."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE avaliacao
        SET nota = %s
        WHERE id = %s
        """,
        (nota, avaliacao_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return "Nota atualizada"


@tool
def atualizar_feedback(avaliacao_id: int, feedback: str):
    """Atualiza feedback e finaliza avaliação."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE avaliacao
        SET feedback_ia = %s,
            status = 'corrigida'
        WHERE id = %s
        """,
        (feedback, avaliacao_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return "Feedback atualizado"