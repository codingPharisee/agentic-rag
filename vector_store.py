rom langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client
import os # loading env variables
from dotenv import load_dotenv, dotenv_values

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TABLE_NAME ="documents"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

embeddings = OpenAiEmbeddings(model="text-embedding-3-small")

vector_store = SupabaseVectorStore(
    embedding - embeddings, client = supabase, table_name = "documents"

)

def add_documents(texts:list[str]):
    docs = [Document(page_content = text, metadata={"content_type": "text"}) for text in texts]

    SupabaseVectorStore.from_documents(
    documents = docs ,
    embedding = embeddings ,
    client = supabase ,
    table_name = TABLE_NAME ,
    query_name = "match_documents",
     )

def get_vecto_store()-> SupabaseVectoreStore:
    return SupabaseVectorStore(
        embedding = embeddings,
        client = supabase,
        table_name = TABLE_NAME, 
        query_name = "match_documents",
    )
def retrieve(query: str, k: int = 2)->list[str]:
    vs = get_vector_store()
    