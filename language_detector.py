import fasttext
import os

class LanguageDetector:
    def __init__(self, model_path="lid.176.bin"):
        self.model = fasttext.load_model(model_path)

    def detect(self, text):
        prediction = self.model.predict(text.replace("\n", " "))
        return prediction[0][0].replace("__label__", "")