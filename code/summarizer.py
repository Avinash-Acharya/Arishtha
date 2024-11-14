import time
import torch
from transformers import AutoTokenizer, BartForConditionalGeneration

fb = "models/bart_cnn_text_summarization"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BartForConditionalGeneration.from_pretrained(fb)
tokenizer = AutoTokenizer.from_pretrained(fb)
model.to(device)

def summarize(allPara):

    start = time.time()

    inputs = tokenizer(allPara,max_length=1024, truncation=True, padding="longest", return_tensors="pt")
    input_length = inputs['input_ids'].shape[1]
    max_summary_length = min(int(input_length * 0.3), 400)
    min_summary_length = max(int(input_length * 0.1), 100)
    summary_ids = model.generate(inputs["input_ids"], min_length=min_summary_length, max_length=max_summary_length)
    result = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    
    end = time.time()
    time_taken = end - start
    print(f"Time taken to summarize: {time_taken:.2f} seconds")

    return result