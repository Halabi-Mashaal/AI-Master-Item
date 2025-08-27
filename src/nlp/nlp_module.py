# NLP-related code for Master Item AI Agent

import spacy
from transformers import pipeline

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load transformers pipeline for zero-shot classification
classifier = pipeline("zero-shot-classification")

def parse_request(request_text):
    """
    Parse the request text using spaCy.
    """
    doc = nlp(request_text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def classify_request(request_text, labels):
    """
    Classify the request text into predefined labels using transformers.
    """
    result = classifier(request_text, labels)
    return result

if __name__ == "__main__":
    # Example usage
    request = "Optimize inventory for item 12345"
    labels = ["inventory", "planning", "optimization"]
    print("Entities:", parse_request(request))
    print("Classification:", classify_request(request, labels))
