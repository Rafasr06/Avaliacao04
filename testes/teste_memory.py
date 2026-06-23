from memory.memory_manager import memory_manager


memory_manager.adicionar_mensagem_global(
    1,
    "Quero estudar Python"
)


memory_manager.adicionar_mensagem_global(
    1,
    "Explique funções"
)



print("MEMÓRIA GLOBAL")
print(
    memory_manager.buscar_memoria_global(1)
)



memory_manager.adicionar_mensagem_materia(
    1,
    2,
    "Como funciona uma lista em Python?"
)



memory_manager.adicionar_mensagem_materia(
    1,
    2,
    "Explique tuplas"
)



print("\nMEMÓRIA PYTHON")
print(
    memory_manager.buscar_memoria_materia(
        1,
        2
    )
)