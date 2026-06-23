from tools.topico_tools import (
    concluir_topico,
    verificar_topico_concluido
)

from tools.avaliacao_tools import (
    criar_avaliacao,
    atualizar_nota,
    atualizar_feedback
)


def finalizar_topico(
    aluno_id,
    materia_id,
    topico_id,
    titulo_topico
):

    ja_concluido = verificar_topico_concluido.invoke(
        {
            "aluno_id": aluno_id,
            "topico_id": topico_id
        }
    )

    if ja_concluido:
        return "Este tópico já foi concluído anteriormente."


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
            "titulo": titulo_topico
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
            "feedback": "Aluno concluiu o tópico com sucesso."
        }
    )


    return "Tópico concluído e avaliação registrada."