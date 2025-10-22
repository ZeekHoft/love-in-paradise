from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


model = AutoModelForSequenceClassification.from_pretrained(
    "cross-encoder/nli-deberta-v3-small"
    # "cross-encoder/nli-MiniLM2-L6-H768"
)
tokenizer = AutoTokenizer.from_pretrained(
    "cross-encoder/nli-deberta-v3-small"
    # "cross-encoder/nli-MiniLM2-L6-H768"
)


def calculate_entailment(claim, sentences) -> list[dict]:
    """
    Checks if facts on the evidence are consistent with the claim.

    Returns a list of the label and score of each sentence.
    """
    sentence_combinations = [[sentence, claim] for sentence in sentences]

    features = tokenizer(
        sentence_combinations,
        padding=True,
        truncation=True,
        return_tensors="pt",
    )

    model.eval()
    with torch.no_grad():
        scores = model(**features).logits
        label_mapping = ["contradiction", "entailment", "neutral"]
        labels = []
        max_scores = scores.argmax(dim=1)
        for i in range(len(scores)):
            top_score = max_scores[i]
            score = scores[i][top_score]
            label = label_mapping[top_score]
            labels.append(
                {
                    "label": label,
                    "score": score.item(),
                    "sentence": sentences[i],
                }
            )
        return labels
