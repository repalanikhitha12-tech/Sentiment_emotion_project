# Task 9 – Advanced ML Validation & Performance Testing

## Evaluation Setup
- Controlled test cases: 3
- Recommendations evaluated: Top 3
- Baseline: Original recommendation dataset order
- Advanced: Existing personalized + hybrid + ranking pipeline
- Relevance labels: Manually defined for testing

## Average Metrics

| Metric | Baseline | Advanced |
|---|---:|---:|
| Precision@3 | 0.444 | 0.667 |
| Recall@3 | 0.556 | 0.889 |
| F1@3 | 0.489 | 0.756 |
| NDCG@3 | 0.486 | 0.922 |
| Diversity | 1.000 | 1.000 |

## Response Time
Average measured response time: 0.051 ms.

This is a local test measurement, not a production performance guarantee.

## Observations
- Advanced metrics were higher in this controlled dataset.
- High-fear case produced the same top-3 results in baseline and advanced.
- Sadness and joy cases showed higher relevance metrics with the advanced pipeline.
- Diversity was equal in both approaches.

## Limitations
- Only 3 manually labeled cases were used.
- Relevance labels are not real user ratings.
- Real user acceptance rate was not measured.
- Results do not establish general performance on unseen users or data.

## Conclusion
The initial controlled evaluation showed higher Precision@3,
Recall@3, F1@3, and NDCG@3 for the advanced pipeline.
More diverse test cases and actual user feedback are needed
for stronger validation.

## Feedback Evaluation

A sample feedback evaluation was performed using four test records.

| Metric | Result |
|---|---:|
| Total feedback records | 4 |
| Liked | 2 |
| Disliked | 2 |
| Acceptance rate | 50% |

Acceptance rate was calculated as:

Acceptance Rate = (Liked / Total Feedback) × 100

The feedback evaluation code ran successfully. These records are sample data, not actual user feedback.

## Regression Testing

The existing Milestone 3 test suite was executed.

- Tests passed: 32
- Tests failed: 0
- Execution time: 0.09 seconds

## Limitation

The current recommendation system uses a hybrid rule-based scoring and ranking pipeline. These results validate the implemented workflow on controlled test cases; they do not establish that an advanced ML model outperforms the baseline.