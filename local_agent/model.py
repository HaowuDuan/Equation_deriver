from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time
model=OllamaLLM(model="llama3.2")

template="""You are an expert in answering questions about a pizza restaurant

Here are some relevant reviews :{review}

Here is the question to answer:{question}
"""

prompt=ChatPromptTemplate.from_template(template)
chain=prompt|model 

while True:
    print("\n\n--------------------------------------")
    question=input("Ask your question(q to quit):")
    print("\n\n--------------------------------------")
    if question=="q":
        break
    result=chain.invoke({"review":[],"question":question})
    print(result)
# t0=time.time()

# t1=time.time()

# print(f"response time:{t1-t0}"s)