from langchain_core.tools import tool
from database.connection import get_connection


@tool
def salvar_mensagem(materia_id: int, role: str, conteudo: str):
    """Salva conversa no histórico."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO historico_conversa (materia_id, role, conteudo)
        VALUES (%s, %s, %s)
        """,
        (materia_id, role, conteudo)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return "Mensagem salva"


@tool
def buscar_contexto_materia(materia_id: int):
    """Busca últimas mensagens da matéria."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, conteudo
        FROM historico_conversa
        WHERE materia_id = %s
        ORDER BY criado_em DESC
        LIMIT 10
        """,
        (materia_id,)
    )

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados