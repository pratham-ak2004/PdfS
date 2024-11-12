from transformers import pipeline

class Models:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization", model="pszemraj/led-base-book-summary", device="cuda"
        )  # https://huggingface.co/pszemraj/led-base-book-summary
        self.qna = pipeline(
            "question-answering", model="deepset/roberta-base-squad2", device="cuda"
        )  # https://huggingface.co/deepset/roberta-base-squad2
        self.qna_input = {
            "question": "",
            "context": ""
        }
    
    def summarize(self, text, max_length=1000, min_length=100):
        summary = self.summarizer(text, max_length=max_length, min_length=min_length)

        return summary
    
    def qna(self, question, context):
        self.qna_input = {
            "question": question,
            "context": context
        }
        result = self.qna(question=question, context=context)

        return result