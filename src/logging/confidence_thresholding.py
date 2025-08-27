# Confidence score thresholding for Master Item AI Agent

def assign_confidence_score(predictions):
    """
    Assign confidence scores to predictions.
    """
    confidence_scores = [pred["score"] for pred in predictions]
    return confidence_scores

def route_request_based_on_confidence(predictions, threshold=0.8):
    """
    Route requests based on confidence scores.
    """
    for pred in predictions:
        if pred["score"] >= threshold:
            print(f"Routing request: {pred['label']} with confidence {pred['score']}")
        else:
            print(f"Flagging request for review: {pred['label']} with confidence {pred['score']}")

if __name__ == "__main__":
    # Example usage
    example_predictions = [
        {"label": "inventory", "score": 0.9},
        {"label": "planning", "score": 0.6}
    ]
    route_request_based_on_confidence(example_predictions)
