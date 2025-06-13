from transformers import pipeline

# Load zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Function to classify input as a news claim or not
def classify_input(text):
    candidate_labels = ["news claim", "opinion", "question", "statement", "gibberish"]
    result = classifier(text, candidate_labels)

    # Print ranked labels and confidence scores
    print(f"\nInput: {text}")
    for label, score in zip(result["labels"], result["scores"]):
        print(f"{label}: {score:.2f}")

    # Return top label
    return result["labels"][0]

# List of sample inputs
test_inputs = [
    "the president of UK has been abducted and was last seen at the london gate bridge",
    "I've seen bigfoot there in the forest from florida man"
]

# Classify each input and print the result
for text in test_inputs:
    top_label = classify_input(text)
    print(f"Classified as: {top_label}")





