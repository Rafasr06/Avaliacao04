from workflows.graph import app


resultado = app.invoke(
    {
        "student_id": 1,
        "message": "Explique normalização em banco de dados",
        "current_subject": None,
        "completed_topics": [],
        "current_topic": None,
        "conversation_history": [],
        "last_agent": None,
        "response": "",
        "next_agent": ""
    }
)


print("\nRESPOSTA:")
print(resultado["response"])

print("\nÚLTIMO AGENTE:")
print(resultado["last_agent"])