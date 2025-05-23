from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

model_path = r"C:\Users\s\.cache\huggingface\hub\models--deepset--xlm-roberta-large-squad2\snapshots\dafe59921a75cdffc06ed3ad6e45c581b22b85cc"

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForQuestionAnswering.from_pretrained(model_path, local_files_only=True, ignore_mismatched_sizes=True)

def answer_question(question, context):
    if not question or not context:
        return "⚠️ يرجى إدخال سؤال ونص صالحين."

    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt", truncation=True, max_length=512)
    input_ids = inputs["input_ids"].tolist()[0]

    with torch.no_grad():
        outputs = model(**inputs)
        answer_start = torch.argmax(outputs.start_logits)
        answer_end = torch.argmax(outputs.end_logits) + 1

    if answer_start >= answer_end:
        return "⚠️ لا توجد إجابة واضحة."

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    return answer.strip()
