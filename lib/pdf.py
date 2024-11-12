from lib.model import Models
from gradio import Warning, Info
import pyttsx3 as tts
import pypdf as PDF
import re, os

class Pdf:
    def __init__(self):
        self.pdf_path = ""
        self.pdf = None
        self.models = Models()

        self.start_page = 0
        self.end_page = None
        self.threshold = 5000
        self.engine = tts.init()
        self.voice = self.engine.getProperty("voices")[0]

    def process_pdf_text(self, start_page=0, end_page=None):
        if self.pdf is None:
            return None
        
        if end_page is None or end_page > self.pdf.get_num_pages() or end_page <= start_page:
            end_page = self.pdf.get_num_pages()

        text = ""

        for i in range(start_page, end_page, 1):
            try:
                page = self.pdf.get_page(i)
                page = page.extract_text()
                page = re.sub(r"[\n\t]", "", page)
                text += page.lower() + " "       
            except:
                print("Error at page : ", i)

        return text
    
    def get_text_within_threshold(self, full_text):
        text = ""

        for sentence in full_text.split(". "):
            if len(text + sentence) <= self.threshold:
                text += sentence + ". "
            else:
                break
        
        return text


    def load_pdf(self, value):
        if os.path.exists(value):
            self.pdf_path = value
            self.pdf = PDF.PdfReader(self.pdf_path)
        else:
            Warning("File not found")

    def summmarize(self, max_length=100, min_length=50):
        text = self.process_pdf_text(start_page=self.start_page, end_page=self.end_page)
        text = self.get_text_within_threshold(text)
        summary = self.models.summarize(text, max_length, min_length)

        return summary[0]["summary_text"]
    
    def ask_question(self, question):
        doc = self.process_pdf_text(start_page=self.start_page, end_page=self.end_page)
        result = self.models.qna(question, doc)

        return result
    
    def read_pdf(self):
        text = self.process_pdf_text(start_page=self.start_page, end_page=self.end_page)
        self.engine.setProperty("rate", 150)
        self.engine.save_to_file(text, "./read_file.mp3")
        self.engine.runAndWait()
        return "./read_file.mp3"
    
    def get_avaliable_voices(self):
        voices = list()

        for voice in self.engine.getProperty("voices"):
            voices.append(voice.name)

        return voices

    def set_voice(self, value):
        for voice in self.engine.getProperty("voices"):
            if voice.name == value:
                self.voice = voice
                self.engine.setProperty("voice", self.voice.id)
                Info("voice set to {}".format(value))
                break