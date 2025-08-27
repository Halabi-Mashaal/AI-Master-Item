# Active learning for Master Item AI Agent

def flag_ambiguous_requests(requests, threshold=0.5):
    """
    Flag ambiguous requests for human review.
    """
    flagged_requests = [req for req in requests if req["confidence"] < threshold]
    return flagged_requests

if __name__ == "__main__":
    # Example usage
    example_requests = [
        {"request": "Optimize inventory", "confidence": 0.4},
        {"request": "Plan delivery", "confidence": 0.9}
    ]
    flagged = flag_ambiguous_requests(example_requests)
    print("Flagged Requests:", flagged)
