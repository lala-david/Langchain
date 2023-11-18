import unittest
from chat_interface import setup_chatbot
from data_loader import load_and_process_pdf_data

class TestSetupChatbot(unittest.TestCase):
    def test_setup_chatbot(self):
        doc, title = load_and_process_pdf_data('./src/pdf/ko_wikipedia_org_NewJeans.pdf')
        chain = setup_chatbot([doc])
        self.assertIsNotNone(chain)

if __name__ == '__main__':
    unittest.main()
