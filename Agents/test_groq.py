
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.1-8b-instant")
response = llm.invoke("Say hello in one sentence.")
print(response.content)