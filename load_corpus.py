from vector_store import add_documents
from langchain_community.document_loaders.parsers.pdf import PyPDFParser
from langchain_core.documents.base import Blob
from langchain_text_splitters import RecursiveCharacterTextSplitter

blob = Blob.from_path("Brian resume.pdf")

parser = PyPDFParser()

docs = parser.lazy_parse(blob)

documents = []

for d in docs:
    documents.append(d)
    print(documents)

text_splitter = RecursiveCharacterTextSplitter(chunk_size= 200, chunk_overlap = 40)

chunks = text_splitter.split_documents(docs)


