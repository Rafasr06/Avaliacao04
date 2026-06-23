from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-5.4-mini")

resposta = llm.invoke("Quem foi campeão da copa do mundo de 2022")

print(resposta.content)

