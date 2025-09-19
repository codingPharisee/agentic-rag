''' 
STEPS
1. setting the sysstem environment
2. setting up the supabase vector database
3. creat documents and loading to vectoer darabase
4. create the agentic rag
5. deploy langraph server
  '''
'''
python environment python -m venv env_name
acivate . envname/scripts/activate
'''
'''
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

-- creating table
DROP TABLE IF EXISTS public.documents;
CREATE TABLE public.documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text NOT NULL,
  metadata jsonb ,
  embedding vector(1536) -- length of vector openai embeddings
);
  
--creating index to enable fast search
CREATE INDEX ON public.documents
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
  
-- function for fetching the relevant entries rpc (remote procedue call)
DROP FUNCTION IF EXISTS public.match_documents(jsonb, vector);
CREATE FUNCTION public.match_documents(
  filter jsonb,
  query_embedding vector(1536)
)
RETURNS TABLE(
  id uuid,
  content text,
  metadata jsonb,
  embedding vector(1536)
) AS $$
  SELECT id, content, metadata, embedding
  FROM public.documents
  WHERE (filter = '{}' OR metadata @> filter)
  ORDER BY embedding <-> query_embedding;
$$ LANGUAGE sql STABLE;
  
'''

langcahainsupabase vector store allows interactin between langchain and supabase