import subprocess
import gradio as gr
from data_loader import load_and_process_pdf_data
from chat_interface import setup_chatbot
from dotenv import load_dotenv 
from urllib.parse import urlparse
import os

load_dotenv()

def create_pdf_from_docs(url, output_filename):
    subprocess.run(["node", "./pdf_creator.js", url, output_filename], check=True)

with open('./www/list.txt', 'r', encoding='utf-8') as file:
    urls = file.read().splitlines()

pdf_filenames = []
for url in urls:
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.replace('.', '_')
    path_name = os.path.basename(parsed_url.path)
    pdf_filename = f"{domain_name}_{path_name}.pdf"
    
    create_pdf_from_docs(url, pdf_filename)
    pdf_filenames.append("pdf/" + pdf_filename)

docs = []
for pdf_filename in pdf_filenames:
    doc, title = load_and_process_pdf_data(pdf_filename)
    docs.extend(doc)

def main():
    chatbot_chain = setup_chatbot(docs)
    chat_history = [] 

    def respond(message):
        nonlocal chatbot_chain   
        nonlocal chat_history  
        if not message:   
            return []  

        result = chatbot_chain(message)
        bot_message = result['answer']
        chat_history.append(("😎 유저", message))   
        chat_history.append(("🐸 챗봇", bot_message))   
        return chat_history

    with open('./style/styles.css', 'r') as file:
        css = file.read()

    with gr.Blocks(css=css) as demo:
        chatbot = gr.Chatbot(label="채팅창")
        msg = gr.Textbox(label="입력")
        clear = gr.Button("초기화")

        msg.submit(respond, inputs=msg, outputs=chatbot)
        clear.click(lambda: None, None, chatbot, queue=False)

        demo.launch(debug=True)

if __name__ == "__main__":
    main()