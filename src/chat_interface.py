import gradio as gr
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

chat_history = []  

def setup_chatbot(docs):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    system_template = """
    Use the following pieces of context to answer the users question shortly.
    Given the following summaries of a long document and a question, create a final answer with references ("SOURCES"),
    ----------------
    {summaries}
    
    You MUST answer in Korean and in Markdown format:"""
    
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    return chain

def respond(message):
    global chatbot_chain   
    global chat_history   

    if not message:   
        return []   

    result = chatbot_chain(message)
    bot_message = result['answer']
    chat_history.append(("user", message))   
    chat_history.append(("bot", bot_message))   
    return chat_history