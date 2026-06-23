# Avaliação 4 - Sistema Multi-Agente de Ensino com IA

## Descrição

Este projeto implementa uma plataforma digital de ensino utilizando uma arquitetura **multi-agente baseada em Inteligência Artificial**.

O sistema utiliza agentes especializados por área de conhecimento, onde um **agente orquestrador** recebe as mensagens do aluno, identifica a intenção e direciona cada solicitação para o agente especialista responsável.

A aplicação foi desenvolvida utilizando:

- Python
- LangChain
- LangGraph
- OpenAI API
- PostgreSQL
- Psycopg

O sistema possui integração com banco de dados para persistência de:

- Histórico de conversas;
- Progresso do aluno;
- Conclusão de tópicos;
- Avaliações;
- Feedbacks.


---

# Arquitetura do Sistema

Fluxo principal da aplicação:

```
                Aluno
                  |
                  v
          Agente Orquestrador
                  |
        +---------+----------+
        |                    |
        v                    v
   Secretário       Agentes Especialistas
                            |
        +-------------------+------------------+
        |          |          |                |
        v          v          v                v
     Python     Banco    Algoritmos     Engenharia
     
                            |
                            v

                      PostgreSQL
```


---

# Agentes Implementados

## Agente Orquestrador

Responsável por:

- Receber mensagens do aluno;
- Identificar a intenção da solicitação;
- Escolher o agente adequado;
- Controlar a matéria atualmente ativa;
- Controlar regras de navegação entre matérias;
- Gerenciar o estado do workflow.


---

# Agente Secretário

Responsável pelas operações administrativas da plataforma.

Funções:

- Consultar dados do aluno;
- Operações administrativas;
- Controle de matrícula;
- Consulta de progresso.


---

# Agentes Especialistas

Cada agente possui um escopo próprio de conhecimento.


## Python Agent

Responsável por conteúdos relacionados a:

- Python;
- Funções;
- Classes;
- Variáveis;
- Conceitos da linguagem.


---

## Banco de Dados Agent

Responsável por:

- SQL;
- SELECT;
- JOIN;
- Normalização;
- Modelagem relacional;
- Conceitos de banco de dados.


---

## Algoritmos Agent

Responsável por:

- Algoritmos;
- Estruturas condicionais;
- Laços de repetição;
- Lógica de programação.


---

## Engenharia de Software Agent

Responsável por:

- UML;
- Requisitos;
- Casos de uso;
- Testes de software.


---

# Persistência de Dados

O sistema utiliza PostgreSQL para armazenar informações da plataforma.

Tabelas utilizadas:

- aluno
- materia
- topico
- topico_aluno
- matricula
- avaliacao
- historico_conversa


---

# Tools (Ferramentas)

Os agentes possuem ferramentas integradas ao banco de dados.


## Tópicos

Ferramentas:

- Buscar tópicos da matéria;
- Registrar conclusão de tópico;
- Consultar progresso do aluno.


---

## Avaliações

Ferramentas:

- Criar avaliação;
- Registrar nota;
- Salvar feedback.


---

# Controle de Progresso

O sistema permite acompanhar a evolução do aluno através dos tópicos concluídos.


Exemplo:

Entrada:

```
concluir topico
```

Fluxo:

```
Aluno
 |
 v
Agente Especialista
 |
 v
Registrar conclusão do tópico
 |
 v
Criar avaliação
 |
 v
Salvar nota
 |
 v
Salvar feedback
```


Exemplo de resposta:

```
Tópico 'JOIN' concluído.

Avaliação criada com nota 10.
```


A conclusão é persistida no banco de dados.


---

# Controle de Contexto

O sistema mantém informações durante o workflow:

- Identificação do aluno;
- Matéria atual;
- Tópicos concluídos;
- Histórico de mensagens;
- Último agente utilizado.


---

# Regra de Troca de Matéria

O sistema possui uma regra de negócio para impedir troca de matéria antes da conclusão de um tópico.

Exemplo:

Aluno:

```
Quero estudar Python
```

Sistema:

```
Você precisa concluir pelo menos um tópico antes de trocar de matéria.
```


Após concluir um tópico, a troca de matéria é liberada.


---

# Execução

Para executar o projeto:

```bash
python main.py
```


---

# Exemplo de Uso


## Pergunta sobre Banco de Dados

Entrada:

```
Explique JOIN
```

Fluxo:

```
Aluno
 |
 v
Orquestrador
 |
 v
Banco Agent
 |
 v
Resposta sobre JOIN
```


---

## Conclusão de Tópico

Entrada:

```
concluir tópico
```

Fluxo:

```
Banco Agent

    |
    v

Registrar conclusão

    |
    v

Criar avaliação

    |
    v

Salvar nota

    |
    v

Salvar feedback
```


---

# Estrutura do Projeto

```
Avaliacao4

├── agents
│   ├── orchestrator.py
│   ├── secretary_agent.py
│   ├── banco_agent.py
│   ├── python_agent.py
│   ├── algoritmos_agent.py
│   ├── engenharia_agent.py
│   └── evaluation_agent.py
│
├── tools
│   ├── aluno_tools.py
│   ├── matricula_tools.py
│   ├── topico_tools.py
│   ├── avaliacao_tools.py
│   ├── conversa_tools.py
│   ├── contexto_tools.py
│   └── finalizar_topico.py
│
├── database
│   └── connection.py
│
├── workflows
│   └── graph.py
│
├── memory
│   └── memory_manager.py
│
├── testes
│   └── arquivos de testes
│
├── main.py
└── requirements.txt
```


---

# Testes

O projeto contém testes individuais para:

- Agentes;
- Tools;
- Memória;
- Workflow;
- Integração com API.


---

# Tecnologias Utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal |
| LangChain | Construção dos agentes |
| LangGraph | Workflow multi-agente |
| OpenAI API | Modelo de Inteligência Artificial |
| PostgreSQL | Persistência dos dados |
| Psycopg | Comunicação com banco de dados |


---

# Pontos a Melhorar

- Implementar a geração automática de uma avaliação contendo exatamente 3 exercícios após a conclusão de um tópico;
- Implementar correção automática baseada nas respostas dos exercícios;

