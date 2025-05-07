from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent,AgentExecutor
from tools import search_tool,wiki_tool
import 
# load the envirnment variables
load_dotenv()

# set up llm 
llm=ChatOpenAI(model="gpt-4")
response=llm.invoke("What is the date of today?")

class Response(BaseModel):
    topic:str
    summary:str
    source:list[str]
    tools_used:list[str]

parser=PydanticOutputParser(pydantic_object=Response)

prompt=ChatPromptTemplate.from_messages([
         ("system",
          """you are a research assistant that will help generate research paper
          Answer the user query and use necessary tools
          Wraps the output in this format and provide no other text\n{format_instructions}
          """, 
         ),
         ("placeholder","{chat_history}"),
         ("human", "{query}"),
         ("placeholder","{agent_scratchpad}"),
    ]
    ).partial(format_instructions=parser.get_format_instructions())

tools=[search_tool,wiki_tool]
agent=create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_excutor=AgentExecutor(agent=agent,tools=tools,verbose=True)
query=input("What can I help you with?")
raw_reponse=agent_excutor.invoke({"query":query})
 
try:
    structured_response=parser.parse(raw_reponse.get("output"))
    print(structured_response)
except Exception as e:
    print("Error parsing response",e,"raw response:",raw_reponse)    
   