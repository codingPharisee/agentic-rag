import os
from typing import Annotated, Dic, Any
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import chatPromptTemplate
from langchain_core.messages import AIMessage, AnyMessage
from langgraph.graph.messages import add_messages

from vector_store import get_vector_store

OPEN_AI_MODEL = "gpt-4o-mini"

TOP_K =2

class RagState(TypedDict):
    messages: Annotated[list[AnyMessage], add_mesages]
    
vector_store= get_vector_store()
retriever= vector_store.as_retriever(k= TOP_K, filter={'content_type':'text'})
llm= ChatOpenAI(model= OPEN_AI_MODEL)

system_prompt= (
    """you are a strict RAG agent answer only based on retrieved content if not, answer 
        'out of provided context'.
    """
   
)

prompt= ChatPromptTemplate.from_messages([
    ('system', system_prompt),
    ('human', 'context: \n {context} \n\n Question:{question}'),
])

# getting the user input
def extract_last_user(state: RAG_State) -> str:
    for m in reversed(state['messages']):
        if getattr(m, 'type', None) == 'human' or getattr(m, 'type', None)== 'user':
            return getattr(m, 'content', '') or ''
        return ''

# retrieving the context
def retrieve_context(q:str, k:int=TOP_K) -> str:
    if not q:
        return ''
    docs= retriever.get_relevat_documents(q)
    if isinstance(docs, int) and k > 0:
        docs = docs[:k]
    return '\n\n'.join(d.page_content for d in docs)

# combining the question and the context and passing to the messages and outing to the llm       
def answer_node(state: RAGState) -> dict[str, Any]:
    k =  TOP_K
    question = extract_last_user(state)
    context = retrieve_context(question, k)
    messages = prompt.format_messages(context= context, question= question)
    out= llm.invoke(mesages)
    return {'messages' [AIMessages(content= out.content)]}
     
def graph():
    g = STATEGraph(RAGstate)
    g.add_node('answer', answer_node)
    g.add_edge(START, 'answer')
    g.edge('answer', END)
    return g.compile()
    
    