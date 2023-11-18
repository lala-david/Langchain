from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

def load_and_process_pdf_data(pdf_filename):
    loader = PyPDFLoader(pdf_filename)   
    documents = loader.load_and_split()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    title = pdf_filename.split('/')[-1].replace('.pdf', '') 
    return docs, title