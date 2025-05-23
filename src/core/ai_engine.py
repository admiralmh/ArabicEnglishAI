from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from text_processing import clean_arabic_text

model_path = r"C:\Users\s\.cache\huggingface\hub\models--deepset--xlm-roberta-large-squad2\snapshots\dafe59921a75cdffc06ed3ad6e45c581b22b85cc"

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForQuestionAnswering.from_pretrained(model_path, local_files_only=True, ignore_mismatched_sizes=True)

def answer_question(question, text_data):
    text_data = clean_arabic_text(text_data)
    question = question.strip()

    inputs = tokenizer(question, text_data[:512], return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    answer_start = outputs.start_logits.argmax()
    answer_end = outputs.end_logits.argmax() + 1
    answer = tokenizer.decode(inputs["input_ids"][0][answer_start:answer_end])

    return answer.strip() if answer.strip() else "⚠️ لا توجد إجابة واضحة"
