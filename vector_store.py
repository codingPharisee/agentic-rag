from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import *
import os # loading env variables
from dotenv import load_dotenv, dotenv_values

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TABLE_NAME ="documents"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
def add_documents(texts:list[str]):
    docs= [Document(page_content= text, metadata= {"content_type":"text"}) for text in texts]

    SupabaseVectorStore.from_documents(
        documents= docs,
        embedding= embeddings,
        client= supabase,
        table_name= TABLE_NAME,
        query_name= "match_documents",
    )
# instance of the database
def get_vector_store()-> SupabaseVectorStore:
    return SupabaseVectorStore(
        embedding= embeddings,
        client= supabase,
        table_name= TABLE_NAME,
        query_name= "match_documents",
    )

# helper funtion to retrieve the data

def  retrieve(query:str, k: int=2) -> list[str]:
    vs = get_vector_store()
    results = vs.similarity_search(query, k=k, filter= {"content_type":"text"})
    return [doc.page_content for doc in results]

# configure the langgraph.json
