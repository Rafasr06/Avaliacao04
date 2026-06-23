from workflows.graph import app

estado = {
    "student_id": 1,
    "message": "",
    "current_subject": None,
    "completed_topics": [],
    "current_topic": None,
    "conversation_history": [],
    "last_agent": None,
    "response": "",
    "next_agent": ""
}

while True:

    mensagem = input("\nAluno: ")

    if mensagem.lower() == "sair":
        print("Encerrando...")
        break

    estado["message"] = mensagem

    estado = app.invoke(estado)

    print("\nESTADO APÓS O GRAFO:")
    print(estado)

    print("\nAssistente:")
    print(estado["response"])

    print("\nAgente utilizado:")
    print(estado["last_agent"])

    print("\nMatéria atual:")
    print(estado["current_subject"])