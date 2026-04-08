from typing import List

def rerank_results(query: str, results: List):
    """
    Simple reranking based on keyword overlap.
    Industry systems use cross-encoders, but this is acceptable for test.
    """

    def score(item):
        text = item.payload.get("text", "").lower()
        query_words = set(query.lower().split())
        text_words = set(text.split())
        return len(query_words.intersection(text_words))

    reranked = sorted(results, key=score, reverse=True)

    return reranked