from tools.aluno_tools import buscar_aluno
from tools.matricula_tools import listar_materias_aluno
from tools.topico_tools import buscar_topicos, buscar_progresso
from tools.conversa_tools import buscar_contexto_materia


print("==== ALUNO ====")

resultado = buscar_aluno.invoke(
    {
        "aluno_id": 1
    }
)

print(resultado)



print("\n==== MATÉRIAS DO ALUNO ====")

resultado = listar_materias_aluno.invoke(
    {
        "aluno_id": 1
    }
)

print(resultado)



print("\n==== TÓPICOS BANCO DE DADOS ====")

resultado = buscar_topicos.invoke(
    {
        "materia_id": 1
    }
)

print(resultado)



print("\n==== PROGRESSO DO ALUNO ====")

resultado = buscar_progresso.invoke(
    {
        "aluno_id": 1
    }
)

print(resultado)



print("\n==== HISTÓRICO DA MATÉRIA ====")

resultado = buscar_contexto_materia.invoke(
    {
        "materia_id": 1
    }
)

print(resultado)