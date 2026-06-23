from langchain_core.tools import tool
from database.connection import get_connection


@tool
def salvar_contexto_aluno(aluno_id: int, materia: str):
    """
    Salva a matéria atual do aluno.
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO contexto_aluno
        (aluno_id, materia_atual)

        VALUES (%s,%s)

        ON CONFLICT (aluno_id)
        DO UPDATE SET
        materia_atual = EXCLUDED.materia_atual
        """,
        (
            aluno_id,
            materia
        )
    )


    conn.commit()

    cursor.close()
    conn.close()


    return "Contexto salvo"



@tool
def buscar_contexto_aluno(aluno_id:int):
    """
    Busca a matéria atual do aluno.
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT materia_atual
        FROM contexto_aluno
        WHERE aluno_id = %s
        """,
        (aluno_id,)
    )


    resultado = cursor.fetchone()


    cursor.close()
    conn.close()


    if resultado:
        return resultado[0]


    return None