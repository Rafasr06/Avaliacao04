Avaliaçâo 4:
Descrição
Este projeto implementa uma plataforma digital de ensino utilizando uma arquitetura multi-agente baseada em Inteligência Artificial.

O sistema utiliza agentes especializados por área de conhecimento, onde um agente orquestrador é responsável por receber as mensagens do aluno e direcionar cada solicitação para o agente especialista adequado.

A aplicação utiliza:

Python
LangChain
LangGraph
OpenAI API
PostgreSQL
O sistema também possui integração com banco de dados para persistência de:

Histórico de conversas;
Progresso do aluno;
Conclusão de tópicos;
Avaliações;
Feedbacks.
Arquitetura do Sistema
O fluxo principal da aplicação:

Aluno
 |
 v
Orquestrador
 |
 +----------------+
 |                |
 v                v
Secretário     Agentes Especialistas
                  |
                  +----------------+
                  |        |       |
                  v        v       v
               Python   Banco   Algoritmos
               
                    |
                    v

              PostgreSQL
Agentes Implementados
Agente Orquestrador
Responsável por:

Receber mensagens do aluno;
Identificar a intenção da solicitação;
Encaminhar para o agente correto;
Controlar a matéria atualmente ativa;
Controlar regras de troca de matéria.
Agente Secretário
Responsável pelas operações administrativas da plataforma.

Funções:

Consultas administrativas;
Consulta de progresso;
Operações relacionadas ao aluno.
Agentes Especialistas
Cada agente possui um escopo próprio de atuação.

Agentes disponíveis:

Python Agent
Responsável por conteúdos relacionados a:

Python;
Funções;
Classes;
Variáveis;
Conceitos da linguagem.
Banco de Dados Agent
Responsável por:

SQL;
SELECT;
JOIN;
Normalização;
Modelagem relacional;
Conceitos de banco de dados.
Algoritmos Agent
Responsável por:

Algoritmos;
Estruturas condicionais;
Laços de repetição.
Engenharia de Software Agent
Responsável por:

UML;
Requisitos;
Casos de uso;
Testes de software.
Persistência de Dados
O sistema utiliza PostgreSQL para armazenar informações da plataforma.

Tabelas utilizadas:

aluno
materia
topico
topico_aluno
matricula
avaliacao
historico_conversa
Ferramentas (Tools)
Os agentes possuem ferramentas integradas ao banco de dados.

Tópicos
Ferramentas:

Buscar tópicos;
Registrar conclusão de tópico;
Consultar progresso.
Conversas
Ferramentas:

Salvar histórico de mensagens;
Recuperar contexto da matéria.
Avaliações
Ferramentas:

Criar avaliação;
Registrar nota;
Salvar feedback.
Controle de Progresso
O sistema permite registrar a evolução do aluno através dos tópicos concluídos.

Exemplo:

Aluno conclui um tópico:

Aluno:
concluir topico

Sistema:
Tópico 'JOIN' concluído.
Avaliação criada com nota 10.
A conclusão é persistida no banco de dados.

Controle de Contexto
O sistema mantém informações durante o fluxo:

Identificação do aluno;
Matéria atual;
Tópicos concluídos;
Histórico de mensagens;
Último agente utilizado.
Regra de Troca de Matéria
O sistema possui uma regra de negócio que impede troca de matéria antes da conclusão de um tópico.

Exemplo:

Aluno:
Quero estudar Python

Sistema:
Você precisa concluir pelo menos um tópico antes de trocar de matéria.
Execução
Executar:

python main.py
Exemplo de Uso
Pergunta sobre Banco de Dados
Entrada:

Explique JOIN
Fluxo:

Aluno
 |
Orquestrador
 |
Banco Agent
 |
Resposta sobre JOIN
Conclusão de Tópico
Entrada:

concluir topico
Fluxo:

Banco Agent
 |
Registrar conclusão
 |
Criar avaliação
 |
Salvar nota
 |
Salvar feedback
Estrutura do Projeto
# Arquitetura do Projeto

Avaliacao4

├── agents
│ ├── orchestrator.py
│ ├── secretary_agent.py
│ ├── banco_agent.py
│ ├── python_agent.py
│ ├── algoritmos_agent.py
│ └── engenharia_agent.py
│
├── tools
│ ├── aluno_tools.py
│ ├── matricula_tools.py
│ ├── topico_tools.py
│ ├── avaliacao_tools.py
│ ├── conversa_tools.py
│ ├── contexto_tools.py
│ └── finalizar_topico.py
│
├── database
│ └── connection.py
│
├── workflows
│ └── graph.py
│
├── memory
│ └── memory_manager.py
│
├── testes
│ └── arquivos de testes
│
├── main.py
└── requirements.txt

---

# Tecnologias Utilizadas

- Python
- LangChain
- LangGraph
- OpenAI API
- PostgreSQL
- Psycopg

Após concluir um tópico, a troca é liberada.

#testes


contém testes individuais para:

- Agentes;
- Tools;
- Memória;
- Workflow;
- API.

#Tecnologias Utilizadas


| Tecnologia | Uso |
|-|-|
| Python | Linguagem principal |
| LangChain | Construção dos agentes |
| LangGraph | Workflow multi-agente |
| OpenAI API | Modelo de IA |
| PostgreSQL | Persistência dos dados |
| Psycopg | Comunicação com banco |

# Pontos a melhorar 

- Não consegui implementar a geração dos 3 exercicíos após a conclução dos tópicos, avaliação.
