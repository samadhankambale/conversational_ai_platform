def analyze_conversation(history):
    return {
        "length": len(history),
        "engagement_score": min(len(history) / 10, 1.0)
    }