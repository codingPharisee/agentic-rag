from vector_store import add_documents
from langchain_community.document_loaders.parsers.pdf import PyPDFParser
from langchain_core.documents.base import Blob
from langchain_text_splitters import RecursiveCharacterTextSplitter

blob = Blob.from_path("sample.pdf") #blob- (binary large object)- a data type used to store large amounts of 
#binary data, such as images , audio, video,and other files within a database/system. used to store entire files directly.

parser = PyPDFParser()

docs = parser.lazy_parse(blob)

documents = []

for d in docs:
    documents.append(d)
    print(documents)

text_splitter = RecursiveCharacterTextSplitter(chunk_size= 200, chunk_overlap = 40)

chunks = text_splitter.split_documents(documents)

for i, chunk in enumerate(chunks):
    print(f"chunk{i}:{chunk.page_content[:100]}...")
    print(f"Metadata:{chunk.metadata}")
    print("-"* 100)

add_documents([chunk.page_content for chunk in chunks])
print("Documents added to vector store")


