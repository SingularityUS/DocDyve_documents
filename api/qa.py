import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

def answer_question(question, file_paths):
    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
    model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

    # Set the device to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Initialize the best answer and score
    best_answer = ''
    best_score = 0.0

    # Loop over the documents and find the best answer
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            context = f.read().decode('utf-8')

        inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt").to(device)
        input_ids = inputs["input_ids"].tolist()[0]

        outputs = model(**inputs)
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits

        # Find the start and end indices of the answer in the context
        answer_start_index = torch.argmax(answer_start_scores)
        answer_end_index = torch.argmax(answer_end_scores) + 1
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start_index:answer_end_index]))

        # Compute the score for the answer
        score = torch.max(answer_start_scores) + torch.max(answer_end_scores)

        # Update the best answer and score
        if score > best_score:
            best_answer = answer
            best_score = score

    return best_answer