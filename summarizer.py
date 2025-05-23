from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

class AdvancedSummarizer:
    def summarize(self, text, sentences_count=3):
        parser = PlaintextParser.from_string(text, Tokenizer("arabic"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return " ".join(str(sentence) for sentence in summary)
