from transformers import pipeline

class AIEngine:
    def __init__(self):
        self.qa_pipeline = pipeline("question-answering")

    def answer_question(self, question, context):
        result = self.qa_pipeline(question=question, context=context)
        return result['answer']