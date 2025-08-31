from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


model = AutoModelForSequenceClassification.from_pretrained(
    "cross-encoder/nli-deberta-v3-small"
)
tokenizer = AutoTokenizer.from_pretrained("cross-encoder/nli-deberta-v3-small")


class EvidenceAlignment:
    """
    This class focuses on checking if facts on the evidence are consistent with the claim.

    Some uses are calculation for entailment, contractiction, and neutrality.
    """

    def calculate_entailment(self, claim, sentences):
        sentence_combinations = [[claim, sentence] for sentence in sentences]

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
                labels.append((label, score))
            return labels
