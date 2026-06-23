from collections import defaultdict, deque


class MemoryManager:

    def __init__(self, limite=10):
        """
        limite = quantidade de mensagens mantidas na memória
        """

        self.limite = limite


        # Memória global do aluno
        # usada pelo orquestrador
        self.memoria_global = defaultdict(
            lambda: deque(maxlen=self.limite)
        )


        # Memória separada por matéria
        # usada pelos agentes especialistas
        self.memoria_materia = defaultdict(
            lambda: defaultdict(
                lambda: deque(maxlen=self.limite)
            )
        )



    def adicionar_mensagem_global(
        self,
        aluno_id,
        mensagem
    ):
        """
        Salva mensagem no histórico global
        """

        self.memoria_global[aluno_id].append(
            mensagem
        )



    def buscar_memoria_global(
        self,
        aluno_id
    ):
        """
        Retorna últimas mensagens globais
        """

        return list(
            self.memoria_global[aluno_id]
        )



    def adicionar_mensagem_materia(
        self,
        aluno_id,
        materia_id,
        mensagem
    ):
        """
        Salva mensagem somente daquela matéria
        """

        self.memoria_materia[aluno_id][materia_id].append(
            mensagem
        )



    def buscar_memoria_materia(
        self,
        aluno_id,
        materia_id
    ):
        """
        Retorna histórico isolado da matéria
        """

        return list(
            self.memoria_materia[aluno_id][materia_id]
        )



    def limpar_memoria_materia(
        self,
        aluno_id,
        materia_id
    ):
        """
        Limpa contexto de uma matéria
        """

        self.memoria_materia[aluno_id][materia_id].clear()



# Instância única utilizada pelo sistema

memory_manager = MemoryManager()