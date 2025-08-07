from langsmith.evaluation import EvaluationResult, run_evaluator

@run_evaluator
def check_category_match(run, example):
    """ 
    A simple custom evaluator that checks if the predicted category 
    contains the expected category as a substring, case-insensitively. 
    """
    predicted = run.outputs.get("category", "").lower()

    expected = example.outputs.get("expected_category", "").lower()

    score = 1 if expected in predicted else 0

    return EvaluationResult(
        key="category_match_ci",
        score=score
    )
