def compare_metrics(bert_metrics, distilbert_metrics):
    """
    Compare BERT and DistilBERT evaluation metrics.
    """

    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1"
    ]

    comparison = {}

    for metric in metrics:
        bert_score = bert_metrics.get(metric, 0)
        distilbert_score = distilbert_metrics.get(metric, 0)

        if bert_score > distilbert_score:
            better_model = "BERT"
        elif distilbert_score > bert_score:
            better_model = "DistilBERT"
        else:
            better_model = "Equal"

        comparison[metric] = {
            "BERT": bert_score,
            "DistilBERT": distilbert_score,
            "better_model": better_model
        }

    return comparison